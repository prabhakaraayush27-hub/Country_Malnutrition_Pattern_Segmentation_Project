"""
run_pipeline.py
End-to-end unsupervised learning pipeline for country malnutrition pattern segmentation.
Executes:
  1. Data Loading & Audit
  2. 7-Step Documented Preprocessing
  3. K-Means & K-Medians Sweep (K=3..8, 20 restarts)
  4. Common-Ruler Validation & Bootstrap Stability (20 rounds, 80% subsample)
  5. Hierarchical Comparison (Ward, Complete, Average, Single with Euclidean & Manhattan)
  6. PCA Projection & Loadings
  7. Cluster Profiling, Transparent Naming & Borderline Identification
  8. Publication-Quality Figure Generation
  9. Exporting results.json, model_comparison.csv, and frontend/data/results.js
"""

import os
import sys
import json
import argparse
import tempfile
from pathlib import Path

# Set Matplotlib cache dir to temp to prevent permission issues
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, davies_bouldin_score

# Ensure backend directory is in path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    RAW_DATA_PATH,
    RESULTS_JSON_PATH,
    RESULTS_JS_PATH,
    MODEL_COMPARISON_CSV_PATH,
    FIGURES_DIR,
    RANDOM_SEED,
    INDICATORS,
    INDICATOR_MISSING_THRESHOLD,
    COUNTRY_MISSING_THRESHOLD,
    CORRELATION_DROP_THRESHOLD,
    WINSORIZE_LOWER_QUANTILE,
    WINSORIZE_UPPER_QUANTILE,
    INCOME_GROUP_MAPPING,
    K_VALUES,
    MIN_CLUSTER_SIZE_THRESHOLD,
    BORDERLINE_SILHOUETTE_THRESHOLD
)
from metrics import (
    KMedians,
    run_clustering_sweep,
    run_hierarchical_comparison,
    detect_elbow_kneedle
)

def run_pipeline(data_path=None):
    print("=" * 85)
    print("COUNTRY MALNUTRITION PATTERN SEGMENTATION PIPELINE")
    print("Course: Unsupervised Learning | Bill & Melinda Gates Foundation Nutrition Analysis")
    print("=" * 85)

    if data_path is None:
        data_path = RAW_DATA_PATH
    data_path = Path(data_path)

    is_demo = "DEMO" in data_path.name.upper()

    if not data_path.exists():
        print(f"[ERROR] Data file not found at {data_path}. Running fetch_data.py first...")
        from fetch_data import main as fetch_main
        fetch_main()

    df_raw = pd.read_csv(data_path)
    print(f"\n[STEP 0] Raw Data Ingestion: {df_raw.shape[0]} countries, {df_raw.shape[1]} columns loaded from {data_path.name}")
    if is_demo:
        print("  >>> NOTICE: RUNNING ON SYNTHETIC DEMO DATASET <<<")
    else:
        print("  >>> CONFIRMED: RUNNING ON REAL WORLD BANK / JOINT ESTIMATES DATASET <<<")

    # Candidate clustering features (exclude metadata, context GDP, and sex-disaggregated duplicates if total exists)
    candidate_features = [
        "stunting", "wasting", "underweight", "undernourishment",
        "anaemia_children", "anaemia_women", "low_birthweight",
        "exclusive_breastfeeding", "child_overweight", "adult_obesity"
    ]
    # Filter to columns that actually exist in the CSV
    candidate_features = [c for c in candidate_features if c in df_raw.columns]

    # ==========================================================================
    # PREPROCESSING PIPELINE (7 STEPS)
    # ==========================================================================
    print("\n" + "-" * 85)
    print("PREPROCESSING EXECUTION LOG")
    print("-" * 85)

    # Step 1: Drop indicators missing for >40% of countries
    print("[PREPROC STEP 1] Indicator Missingness Audit (Threshold: >40% missing dropped)")
    kept_indicators = []
    dropped_indicators = []
    indicator_missingness_report = {}
    for ind in candidate_features:
        miss_count = int(df_raw[ind].isna().sum())
        miss_pct = float(miss_count / len(df_raw))
        indicator_missingness_report[ind] = {
            "missing_count": miss_count,
            "missing_pct": round(miss_pct * 100, 1),
            "kept": bool(miss_pct <= INDICATOR_MISSING_THRESHOLD)
        }
        if miss_pct <= INDICATOR_MISSING_THRESHOLD:
            kept_indicators.append(ind)
            print(f"  [KEPT]  {ind:<25} missing: {miss_count}/{len(df_raw)} ({miss_pct*100:.1f}%)")
        else:
            dropped_indicators.append(ind)
            print(f"  [DROP]  {ind:<25} missing: {miss_count}/{len(df_raw)} ({miss_pct*100:.1f}%) > {INDICATOR_MISSING_THRESHOLD*100:.0f}%")

    print(f"  -> Retained {len(kept_indicators)} indicators: {kept_indicators}")
    print(f"  -> Dropped {len(dropped_indicators)} indicators: {dropped_indicators}")

    # Step 2: Drop countries missing >50% of the kept indicators
    print(f"\n[PREPROC STEP 2] Country Missingness Pruning (Threshold: >50% of kept indicators missing dropped)")
    country_miss_ratio = df_raw[kept_indicators].isna().mean(axis=1)
    dropped_countries_mask = country_miss_ratio > COUNTRY_MISSING_THRESHOLD
    dropped_countries_df = df_raw[dropped_countries_mask][["country_code", "country_name", "region"]].copy()
    dropped_countries_df["missing_pct"] = (country_miss_ratio[dropped_countries_mask] * 100).round(1)

    df_filtered = df_raw[~dropped_countries_mask].copy().reset_index(drop=True)
    print(f"  -> Dropped {len(dropped_countries_df)} countries missing > {COUNTRY_MISSING_THRESHOLD*100:.0f}% indicators:")
    for _, row in dropped_countries_df.head(10).iterrows():
        print(f"     * {row['country_name']} ({row['country_code']}, {row['region']}): {row['missing_pct']}% missing")
    if len(dropped_countries_df) > 10:
        print(f"     * ... and {len(dropped_countries_df) - 10} more countries (full list preserved in output JSON)")
    print(f"  -> Sovereign countries retained: {len(df_filtered)} countries")

    # Step 3: Correlation pruning (|r| > 0.92, keep first)
    print(f"\n[PREPROC STEP 3] Collinearity & Redundancy Check (Threshold: |r| > {CORRELATION_DROP_THRESHOLD})")
    corr_matrix_initial = df_filtered[kept_indicators].corr()
    pruned_indicators = list(kept_indicators)
    dropped_correlated = []
    
    for i in range(len(kept_indicators)):
        col1 = kept_indicators[i]
        if col1 not in pruned_indicators:
            continue
        for j in range(i + 1, len(kept_indicators)):
            col2 = kept_indicators[j]
            if col2 not in pruned_indicators:
                continue
            r_val = corr_matrix_initial.loc[col1, col2]
            if abs(r_val) > CORRELATION_DROP_THRESHOLD:
                print(f"  [COLLINEAR] {col1} and {col2} have |r| = {abs(r_val):.3f} > {CORRELATION_DROP_THRESHOLD}. Dropping {col2}.")
                pruned_indicators.remove(col2)
                dropped_correlated.append({"kept": col1, "dropped": col2, "correlation": round(float(r_val), 3)})

    if not dropped_correlated:
        print(f"  -> All {len(pruned_indicators)} indicators have pairwise |r| <= {CORRELATION_DROP_THRESHOLD}. None dropped.")
    else:
        print(f"  -> Dropped collinear indicators: {[d['dropped'] for d in dropped_correlated]}")
    features = pruned_indicators

    # Step 4: Missing value imputation (region median, fallback to global median)
    print("\n[PREPROC STEP 4] Missing Value Imputation (Regional median, global median fallback)")
    imputation_stats = {}
    for col in features:
        initial_missing = int(df_filtered[col].isna().sum())
        # Group by region median
        reg_median = df_filtered.groupby("region")[col].transform("median")
        glob_median = float(df_filtered[col].median())
        df_filtered[col] = df_filtered[col].fillna(reg_median).fillna(glob_median)
        final_missing = int(df_filtered[col].isna().sum())
        imputation_stats[col] = {
            "imputed_count": initial_missing,
            "imputed_pct": round((initial_missing / len(df_filtered)) * 100, 1),
            "global_median": round(glob_median, 2)
        }
        print(f"  [IMPUTE] {col:<25} imputed {initial_missing} missing values (global median: {glob_median:.2f})")

    # Step 5: Winsorization at 1st and 99th percentiles
    print(f"\n[PREPROC STEP 5] Outlier Treatment: Winsorization at {WINSORIZE_LOWER_QUANTILE*100:.0f}th and {WINSORIZE_UPPER_QUANTILE*100:.0f}th percentiles")
    winsorize_stats = {}
    for col in features:
        q_low = float(df_filtered[col].quantile(WINSORIZE_LOWER_QUANTILE))
        q_high = float(df_filtered[col].quantile(WINSORIZE_UPPER_QUANTILE))
        n_low_clipped = int((df_filtered[col] < q_low).sum())
        n_high_clipped = int((df_filtered[col] > q_high).sum())
        df_filtered[col] = df_filtered[col].clip(q_low, q_high)
        winsorize_stats[col] = {
            "q01": round(q_low, 3),
            "q99": round(q_high, 3),
            "low_clipped": n_low_clipped,
            "high_clipped": n_high_clipped
        }
        print(f"  [WINSORIZE] {col:<25} range: [{q_low:.2f}, {q_high:.2f}] (clipped: {n_low_clipped} low, {n_high_clipped} high)")

    # Step 6: Categorical encoding (ordinal income 1-4, keep region label)
    # Strictly for profiling - NEVER fed into clustering feature matrix X
    print("\n[PREPROC STEP 6] Categorical Profiling Encoding (Income Group 1-4, Region label preserved)")
    df_filtered["income_group_num"] = df_filtered["income_group"].map(INCOME_GROUP_MAPPING).fillna(0).astype(int)
    print(f"  -> Income Group distribution: {df_filtered['income_group'].value_counts().to_dict()}")
    print(f"  -> Region distribution: {df_filtered['region'].value_counts().to_dict()}")
    print("  -> CRITICAL METHODOLOGICAL CONTROL: Categorical variables are strictly excluded from clustering feature set to prevent circularity.")

    # Step 7: StandardScaler (z-score)
    print("\n[PREPROC STEP 7] Feature Standardization: StandardScaler (z-score normalization)")
    scaler = StandardScaler()
    X = scaler.fit_transform(df_filtered[features])
    print(f"  -> Standardized feature matrix X shape: {X.shape} (zero mean, unit variance)")

    # ==========================================================================
    # CLUSTERING & MODEL COMPARISON SWEEP
    # ==========================================================================
    print("\n" + "=" * 85)
    print("CLUSTERING SWEEP & MODEL SELECTION (K=3..8, Euclidean vs Manhattan)")
    print("=" * 85)

    df_comparison, fitted_models, selected_config_id, kneedle_elbows = run_clustering_sweep(
        X, K_VALUES, random_state=RANDOM_SEED
    )

    print("\n" + df_comparison[[
        "config_id", "distance", "k", "silhouette_euclidean", "davies_bouldin_euclidean",
        "stability_mean_ari", "min_cluster_size", "is_valid", "composite_rank"
    ]].sort_values("composite_rank").to_string(index=False))

    selected_row = df_comparison[df_comparison["config_id"] == selected_config_id].iloc[0]
    selected_k = int(selected_row["k"])
    selected_dist = str(selected_row["distance"])
    print(f"\n[MODEL SELECTION] Selected Final Model: {selected_config_id.upper()}")
    print(f"  - Distance Metric: {selected_dist.capitalize()}")
    print(f"  - Number of Clusters (K): {selected_k}")
    print(f"  - Silhouette Score (Euclidean ruler): {selected_row['silhouette_euclidean']:.4f}")
    print(f"  - Davies-Bouldin Index (Euclidean ruler): {selected_row['davies_bouldin_euclidean']:.4f}")
    print(f"  - Bootstrap Stability (Mean ARI): {selected_row['stability_mean_ari']:.4f} (std: {selected_row['stability_std_ari']:.4f})")
    print(f"  - Minimum Cluster Size: {selected_row['min_cluster_size']} countries (Constraint: >= 5)")
    print(f"  - Kneedle Elbow Points: Euclidean K={kneedle_elbows['euclidean']}, Manhattan K={kneedle_elbows['manhattan']}")

    # Attach all clustering solutions to df_filtered
    for cfg_id, m in fitted_models.items():
        df_filtered[f"cluster_{cfg_id}"] = m.labels_
    selected_labels = fitted_models[selected_config_id].labels_
    df_filtered["cluster"] = selected_labels

    # ==========================================================================
    # HIERARCHICAL CLUSTERING COMPARISON
    # ==========================================================================
    print("\n" + "=" * 85)
    print(f"HIERARCHICAL CLUSTERING BENCHMARK (Cut at K = {selected_k})")
    print("=" * 85)

    df_hierarchical, linkage_matrices, dendrogram_data = run_hierarchical_comparison(
        X, target_k=selected_k, reference_labels=selected_labels
    )
    print("\n" + df_hierarchical.to_string(index=False))

    # ==========================================================================
    # PCA PROJECTION (2 COMPONENTS)
    # ==========================================================================
    print("\n" + "=" * 85)
    print("PRINCIPAL COMPONENT ANALYSIS (Visualisation & Factor Loadings)")
    print("=" * 85)

    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    X_pca = pca.fit_transform(X)
    df_filtered["pca_x"] = np.round(X_pca[:, 0], 4)
    df_filtered["pca_y"] = np.round(X_pca[:, 1], 4)

    explained_var = [round(float(v), 4) for v in pca.explained_variance_ratio_]
    cumulative_var = round(float(np.sum(pca.explained_variance_ratio_)), 4)
    print(f"  - PC1 Explained Variance: {explained_var[0]*100:.2f}%")
    print(f"  - PC2 Explained Variance: {explained_var[1]*100:.2f}%")
    print(f"  - Cumulative 2-Component Variance: {cumulative_var*100:.2f}%")

    loadings_df = pd.DataFrame(
        pca.components_.T,
        index=features,
        columns=["PC1_Loading", "PC2_Loading"]
    ).round(4)
    print("\nPCA Feature Loadings:")
    print(loadings_df)

    # Per-country silhouette
    country_silhouettes = silhouette_samples(X, selected_labels, metric='euclidean')
    df_filtered["silhouette"] = np.round(country_silhouettes, 4)
    df_filtered["is_borderline"] = (country_silhouettes < BORDERLINE_SILHOUETTE_THRESHOLD)
    borderline_df = df_filtered[df_filtered["is_borderline"]]
    print(f"\n[BORDERLINE AUDIT] {len(borderline_df)} borderline countries identified (silhouette < {BORDERLINE_SILHOUETTE_THRESHOLD}):")
    for _, b_row in borderline_df.head(8).iterrows():
        print(f"  * {b_row['country_name']} ({b_row['country_code']}): cluster {b_row['cluster']}, silhouette={b_row['silhouette']:.4f}")

    # ==========================================================================
    # CLUSTER PROFILING & TRANSPARENT NAMING RULE
    # ==========================================================================
    print("\n" + "=" * 85)
    print("CLUSTER INTERPRETATION & TRANSPARENT RULE-BASED NAMING")
    print("=" * 85)

    # Classification of kept features
    undernutrition_cols = [c for c in features if INDICATORS.get(c, {}).get("type") == "undernutrition"]
    overnutrition_cols = [c for c in features if INDICATORS.get(c, {}).get("type") == "overnutrition"]

    cluster_profiles = []
    used_names = set()

    for cl in range(selected_k):
        cl_mask = (selected_labels == cl)
        cl_df = df_filtered[cl_mask]
        cl_size = len(cl_df)
        cl_pct = round((cl_size / len(df_filtered)) * 100, 1)

        # Means
        raw_means = {col: round(float(cl_df[col].mean()), 2) for col in features}
        raw_stds = {col: round(float(cl_df[col].std()), 2) for col in features}
        z_means = {col: round(float(X[cl_mask, i].mean()), 3) for i, col in enumerate(features)}

        # Indices
        under_idx = float(np.mean([z_means[c] for c in undernutrition_cols])) if undernutrition_cols else 0.0
        over_idx = float(np.mean([z_means[c] for c in overnutrition_cols])) if overnutrition_cols else 0.0

        # Transparent naming rule
        if under_idx >= 0.50 and over_idx < 0.20:
            base_name = "High Undernutrition"
        elif over_idx >= 0.40 and under_idx < 0.0:
            base_name = "High Overweight & Obesity"
        elif under_idx >= 0.20 and over_idx >= 0.20:
            base_name = "Double Burden"
        elif under_idx < -0.30 and over_idx < 0.0:
            base_name = "Lower Malnutrition Burden"
        elif under_idx < 0.0 and over_idx >= 0.20:
            base_name = "Emerging Overnutrition / Upper Transition"
        elif under_idx >= 0.15 and over_idx < 0.0:
            base_name = "Moderate Undernutrition / Vulnerable"
        else:
            base_name = "Transitional / Mixed Nutrition"

        # Ensure uniqueness
        cluster_name = base_name
        counter = 2
        while cluster_name in used_names:
            cluster_name = f"{base_name} ({counter})"
            counter += 1
        used_names.add(cluster_name)

        # Typical countries (closest to cluster centroid in X space)
        centroid = fitted_models[selected_config_id].cluster_centers_[cl]
        if selected_dist == "euclidean":
            dists_to_center = np.linalg.norm(X[cl_mask] - centroid, axis=1)
        else:
            dists_to_center = np.sum(np.abs(X[cl_mask] - centroid), axis=1)
        closest_indices = np.argsort(dists_to_center)[:5]
        typical_countries = cl_df.iloc[closest_indices][["country_code", "country_name"]].to_dict(orient="records")

        # Context metrics
        median_gdp = float(cl_df["gdp_per_capita"].dropna().median()) if "gdp_per_capita" in cl_df and not cl_df["gdp_per_capita"].dropna().empty else None
        income_mix = cl_df["income_group"].value_counts().to_dict()
        region_mix = cl_df["region"].value_counts().to_dict()
        mean_sil = round(float(country_silhouettes[cl_mask].mean()), 4)

        # Plain language narrative
        if "Undernutrition" in cluster_name:
            narrative = (
                f"Cluster {cl} is characterized by acute and chronic undernutrition. Average child stunting is "
                f"{raw_means.get('stunting', 0)}% and child wasting is {raw_means.get('wasting', 0)}%, with "
                f"severe child anaemia ({raw_means.get('anaemia_children', 0)}%). It is heavily concentrated in "
                f"{list(region_mix.keys())[0] if region_mix else 'developing regions'} among {list(income_mix.keys())[0] if income_mix else 'low-income'} economies."
            )
        elif "Overweight" in cluster_name or "Obesity" in cluster_name:
            narrative = (
                f"Cluster {cl} represents advanced nutritional transition toward overnutrition. Adult obesity averages "
                f"{raw_means.get('adult_obesity', 0)}% while child stunting is low at {raw_means.get('stunting', 0)}%. "
                f"Countries are predominantly in {list(region_mix.keys())[0] if region_mix else 'urbanized regions'} "
                f"with {list(income_mix.keys())[0] if income_mix else 'higher income'} levels."
            )
        elif "Double" in cluster_name:
            narrative = (
                f"Cluster {cl} exhibits the complex 'double burden of malnutrition', where lingering child stunting "
                f"({raw_means.get('stunting', 0)}%) coexists alongside elevated overweight/obesity rates "
                f"({raw_means.get('adult_obesity', 0)}% adult obesity, {raw_means.get('child_overweight', 0)}% child overweight). "
                f"Requires integrated nutrition policies preventing both deficits and caloric surplus."
            )
        else:
            narrative = (
                f"Cluster {cl} represents an intermediate transitional or lower-burden pattern. Child stunting "
                f"averages {raw_means.get('stunting', 0)}% with adult obesity around {raw_means.get('adult_obesity', 0)}%. "
                f"Countries exhibit mixed health system development across multiple geographic regions."
            )

        profile = {
            "cluster_id": cl,
            "name": cluster_name,
            "size": cl_size,
            "percentage": cl_pct,
            "undernutrition_index": round(under_idx, 3),
            "overnutrition_index": round(over_idx, 3),
            "raw_means": raw_means,
            "raw_stds": raw_stds,
            "z_means": z_means,
            "typical_countries": typical_countries,
            "median_gdp_per_capita": round(median_gdp, 0) if median_gdp is not None else None,
            "income_mix": income_mix,
            "region_mix": region_mix,
            "mean_silhouette": mean_sil,
            "narrative": narrative
        }
        cluster_profiles.append(profile)

        print(f"\nCluster {cl}: '{cluster_name}' (n={cl_size}, {cl_pct}%)")
        print(f"  Indices: Undernutrition Z={under_idx:+.2f}, Overnutrition Z={over_idx:+.2f}")
        print(f"  Median GDP: ${median_gdp:,.0f}" if median_gdp else "  Median GDP: N/A")
        print(f"  Typical countries: {[c['country_name'] for c in typical_countries[:4]]}")
        print(f"  Interpretation: {narrative[:120]}...")

    # Map cluster names back to df_filtered
    name_map = {p["cluster_id"]: p["name"] for p in cluster_profiles}
    df_filtered["cluster_name"] = df_filtered["cluster"].map(name_map)

    # ==========================================================================
    # GENERATE PUBLICATION-QUALITY FIGURES (PNG)
    # ==========================================================================
    print("\n" + "=" * 85)
    print("GENERATING PUBLICATION-QUALITY VISUALIZATION FIGURES")
    print("=" * 85)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Figure 1: Model Selection Panels
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('#0f172a')
    
    # 1A: WCSS & WCSD Elbow
    ax = axes[0, 0]
    ax.set_facecolor('#1e293b')
    sub_euc = df_comparison[df_comparison["distance"] == "euclidean"].sort_values("k")
    sub_man = df_comparison[df_comparison["distance"] == "manhattan"].sort_values("k")
    ax.plot(sub_euc["k"], sub_euc["wcss"], 'o-', color='#38bdf8', lw=2.2, label='Euclidean WCSS')
    ax.axvline(kneedle_elbows['euclidean'], color='#38bdf8', ls='--', alpha=0.7, label=f'Kneedle Elbow (K={kneedle_elbows["euclidean"]})')
    ax.set_title("Inertia / WCSS Elbow Curve", color='#f8fafc', fontsize=12, fontweight='bold')
    ax.set_xlabel("Number of Clusters (K)", color='#94a3b8')
    ax.set_ylabel("Within-Cluster Sum of Squares", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.5)
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    # 1B: Silhouette
    ax = axes[0, 1]
    ax.set_facecolor('#1e293b')
    ax.plot(sub_euc["k"], sub_euc["silhouette_euclidean"], 'o-', color='#38bdf8', lw=2.2, label='Euclidean KMeans')
    ax.plot(sub_man["k"], sub_man["silhouette_euclidean"], 's--', color='#f43f5e', lw=2.0, label='Manhattan KMedians')
    if selected_dist == "euclidean":
        ax.scatter([selected_k], [selected_row['silhouette_euclidean']], color='#fbbf24', s=160, zorder=5, edgecolors='white', label=f'Selected (K={selected_k})')
    else:
        ax.scatter([selected_k], [selected_row['silhouette_euclidean']], color='#fbbf24', s=160, zorder=5, edgecolors='white', label=f'Selected (K={selected_k})')
    ax.set_title("Silhouette Score (Common Euclidean Ruler)", color='#f8fafc', fontsize=12, fontweight='bold')
    ax.set_xlabel("Number of Clusters (K)", color='#94a3b8')
    ax.set_ylabel("Mean Silhouette Score", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.5)
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    # 1C: Davies-Bouldin
    ax = axes[1, 0]
    ax.set_facecolor('#1e293b')
    ax.plot(sub_euc["k"], sub_euc["davies_bouldin_euclidean"], 'o-', color='#38bdf8', lw=2.2, label='Euclidean KMeans')
    ax.plot(sub_man["k"], sub_man["davies_bouldin_euclidean"], 's--', color='#f43f5e', lw=2.0, label='Manhattan KMedians')
    ax.set_title("Davies-Bouldin Index (Lower is Better)", color='#f8fafc', fontsize=12, fontweight='bold')
    ax.set_xlabel("Number of Clusters (K)", color='#94a3b8')
    ax.set_ylabel("Davies-Bouldin Index", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.5)
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    # 1D: Bootstrap Stability
    ax = axes[1, 1]
    ax.set_facecolor('#1e293b')
    ax.errorbar(sub_euc["k"], sub_euc["stability_mean_ari"], yerr=sub_euc["stability_std_ari"], fmt='o-', color='#38bdf8', lw=2.2, capsize=4, label='Euclidean ARI')
    ax.errorbar(sub_man["k"], sub_man["stability_mean_ari"], yerr=sub_man["stability_std_ari"], fmt='s--', color='#f43f5e', lw=2.0, capsize=4, label='Manhattan ARI')
    ax.set_title("Bootstrap Stability (Mean ARI +/- Std, 20 Subsamples)", color='#f8fafc', fontsize=12, fontweight='bold')
    ax.set_xlabel("Number of Clusters (K)", color='#94a3b8')
    ax.set_ylabel("Adjusted Rand Index", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.5)
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    plt.tight_layout()
    fig_path_1 = FIGURES_DIR / "model_selection_panels.png"
    plt.savefig(fig_path_1, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"  [SAVED] {fig_path_1.name}")

    # Figure 2: PCA Projection Scatter with Biplot Vectors
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    
    palette = ['#f43f5e', '#38bdf8', '#10b981', '#a855f7', '#f59e0b', '#ec4899', '#06b6d4', '#84cc16']
    for cl in range(selected_k):
        sub = df_filtered[df_filtered["cluster"] == cl]
        c_color = palette[cl % len(palette)]
        c_label = f"C{cl}: {name_map[cl]} (n={len(sub)})"
        ax.scatter(sub["pca_x"], sub["pca_y"], color=c_color, s=70, alpha=0.85, edgecolors='white', lw=0.5, label=c_label)
        
    # Annotate typical countries
    for p in cluster_profiles:
        for tc in p["typical_countries"][:2]:
            c_row = df_filtered[df_filtered["country_code"] == tc["country_code"]].iloc[0]
            ax.annotate(
                c_row["country_name"],
                (c_row["pca_x"], c_row["pca_y"]),
                xytext=(5, 5), textcoords='offset points',
                color='#f8fafc', fontsize=8.5, weight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='#0f172a', alpha=0.75, edgecolor='#475569', lw=0.5)
            )

    # Feature loadings vectors (biplot)
    scale_factor = 3.5
    for i, f_name in enumerate(features):
        vx = pca.components_[0, i] * scale_factor
        vy = pca.components_[1, i] * scale_factor
        ax.arrow(0, 0, vx, vy, color='#fbbf24', alpha=0.75, width=0.03, head_width=0.12, length_includes_head=True)
        ax.text(vx * 1.12, vy * 1.12, f_name.replace('_', ' '), color='#fbbf24', fontsize=8.5, weight='semibold', ha='center', va='center')

    ax.set_title(f"PCA Visualisation of Country Malnutrition Profiles ({selected_config_id.upper()}, Total Variance: {cumulative_var*100:.1f}%)", color='#f8fafc', fontsize=13, fontweight='bold')
    ax.set_xlabel(f"Principal Component 1 ({explained_var[0]*100:.1f}% Variance Explained - Undernutrition Axis)", color='#94a3b8')
    ax.set_ylabel(f"Principal Component 2 ({explained_var[1]*100:.1f}% Variance Explained - Chronic vs Acute / Obesity Axis)", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.4)
    ax.axhline(0, color='#475569', lw=0.8, ls=':')
    ax.axvline(0, color='#475569', lw=0.8, ls=':')
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0', loc='lower right')

    plt.tight_layout()
    fig_path_2 = FIGURES_DIR / "pca_scatter.png"
    plt.savefig(fig_path_2, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"  [SAVED] {fig_path_2.name}")

    # Figure 3: Dendrogram
    from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    
    Z_ward = linkage_matrices["Ward (Euclidean)"]
    cut_h = dendrogram_data["Ward (Euclidean)"]["cut_height"]
    scipy_dendrogram(
        Z_ward,
        ax=ax,
        no_labels=True,
        color_threshold=cut_h,
        above_threshold_color='#64748b'
    )
    ax.axhline(cut_h, color='#f43f5e', ls='--', lw=2.0, label=f'Cut Height = {cut_h:.2f} (K = {selected_k})')
    ax.set_title(f"Hierarchical Clustering Dendrogram (Ward Linkage, Euclidean Distance)", color='#f8fafc', fontsize=13, fontweight='bold')
    ax.set_ylabel("Cluster Distance (Merge Height)", color='#94a3b8')
    ax.set_xlabel("Country Clusters", color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    ax.grid(True, color='#334155', alpha=0.3)
    ax.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0')

    plt.tight_layout()
    fig_path_3 = FIGURES_DIR / "dendrogram.png"
    plt.savefig(fig_path_3, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"  [SAVED] {fig_path_3.name}")

    # Figure 4: Cluster Profile Heatmap
    z_df = pd.DataFrame([p["z_means"] for p in cluster_profiles], index=[f"C{p['cluster_id']}: {p['name']}" for p in cluster_profiles])
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    
    cmap = plt.cm.RdBu_r
    im = ax.imshow(z_df.values, cmap=cmap, aspect='auto', vmin=-1.8, vmax=1.8)
    cbar = fig.colorbar(im, ax=ax, pad=0.03)
    cbar.set_label("Standardized Z-Score Deviation", color='#94a3b8')
    cbar.ax.tick_params(colors='#94a3b8')
    
    ax.set_xticks(range(len(features)))
    ax.set_xticklabels([f.replace('_', '\n') for f in features], color='#94a3b8', fontsize=9.5)
    ax.set_yticks(range(selected_k))
    ax.set_yticklabels(z_df.index, color='#f8fafc', fontsize=10, fontweight='semibold')
    
    for i in range(selected_k):
        for j in range(len(features)):
            val = z_df.values[i, j]
            text_color = "black" if abs(val) < 0.8 else "white"
            ax.text(j, i, f"{val:+.2f}", ha="center", va="center", color=text_color, fontsize=9, fontweight='bold')
            
    ax.set_title("Standardized Health Indicator Profiles by Cluster (Z-Scores)", color='#f8fafc', fontsize=13, fontweight='bold')
    plt.tight_layout()
    fig_path_4 = FIGURES_DIR / "profile_heatmap.png"
    plt.savefig(fig_path_4, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"  [SAVED] {fig_path_4.name}")

    # Figure 5: Feature Correlation Matrix Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    corr_vals = corr_matrix_initial.loc[features, features].values
    im = ax.imshow(corr_vals, cmap='coolwarm', vmin=-1.0, vmax=1.0)
    cbar = fig.colorbar(im, ax=ax, pad=0.03)
    cbar.set_label("Pearson Correlation Coefficient (r)", color='#94a3b8')
    cbar.ax.tick_params(colors='#94a3b8')
    ax.set_xticks(range(len(features)))
    ax.set_xticklabels([f.replace('_', '\n') for f in features], color='#94a3b8', fontsize=8.5)
    ax.set_yticks(range(len(features)))
    ax.set_yticklabels([f.replace('_', ' ') for f in features], color='#f8fafc', fontsize=9)
    for i in range(len(features)):
        for j in range(len(features)):
            r = corr_vals[i, j]
            text_color = "black" if abs(r) < 0.6 else "white"
            ax.text(j, i, f"{r:.2f}", ha="center", va="center", color=text_color, fontsize=8.5)
    ax.set_title("Indicator Correlation Matrix Before Clustering Pruning", color='#f8fafc', fontsize=13, fontweight='bold')
    plt.tight_layout()
    fig_path_5 = FIGURES_DIR / "correlation_matrix.png"
    plt.savefig(fig_path_5, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"  [SAVED] {fig_path_5.name}")

    # ==========================================================================
    # EXPORT RESULTS (CSV, JSON, JS)
    # ==========================================================================
    print("\n" + "=" * 85)
    print("EXPORTING ARTIFACTS")
    print("=" * 85)

    # 1. Model comparison CSV
    MODEL_COMPARISON_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_comparison.to_csv(MODEL_COMPARISON_CSV_PATH, index=False)
    print(f"  [SAVED] {MODEL_COMPARISON_CSV_PATH}")

    # 2. Results Dictionary
    # Build country records for frontend
    country_export = []
    for _, r in df_filtered.iterrows():
        c_dict = {
            "country_code": r["country_code"],
            "country_name": r["country_name"],
            "region": r["region"],
            "income_group": r["income_group"],
            "income_group_num": int(r["income_group_num"]),
            "gdp_per_capita": float(r["gdp_per_capita"]) if pd.notna(r["gdp_per_capita"]) else None,
            "pca_x": float(r["pca_x"]),
            "pca_y": float(r["pca_y"]),
            "silhouette": float(r["silhouette"]),
            "is_borderline": bool(r["is_borderline"]),
            "cluster": int(r["cluster"]),
            "cluster_name": r["cluster_name"],
            "indicators": {col: round(float(r[col]), 2) for col in features}
        }
        # Include alternative cluster assignments for K=3..8 and Manhattan
        for cfg_id in df_comparison["config_id"].tolist():
            if f"cluster_{cfg_id}" in df_filtered:
                c_dict[f"cluster_{cfg_id}"] = int(r[f"cluster_{cfg_id}"])
        country_export.append(c_dict)

    # Indicator metadata dictionary
    indicator_meta_export = {
        col: {
            "name": INDICATORS.get(col, {}).get("name", col.replace('_', ' ').capitalize()),
            "code": INDICATORS.get(col, {}).get("code", ""),
            "type": INDICATORS.get(col, {}).get("type", "other"),
            "description": INDICATORS.get(col, {}).get("description", "")
        }
        for col in features
    }

    results_data = {
        "metadata": {
            "title": "Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering",
            "organization": "Bill & Melinda Gates Foundation (Gates Foundation-funded Global Nutrition Report data)",
            "course": "Unsupervised Learning (Units II, III & IV)",
            "random_seed": RANDOM_SEED,
            "is_demo": is_demo,
            "total_countries_analyzed": len(df_filtered),
            "total_countries_raw": len(df_raw),
            "countries_dropped_count": len(dropped_countries_df),
            "total_indicators_used": len(features),
            "selected_config_id": selected_config_id,
            "selected_k": selected_k,
            "selected_distance": selected_dist,
            "selected_silhouette": round(float(selected_row["silhouette_euclidean"]), 4),
            "selected_davies_bouldin": round(float(selected_row["davies_bouldin_euclidean"]), 4),
            "selected_stability_ari": round(float(selected_row["stability_mean_ari"]), 4),
            "selected_stability_std": round(float(selected_row["stability_std_ari"]), 4),
            "borderline_countries_count": len(borderline_df),
            "kneedle_elbows": kneedle_elbows,
            "pca_variance_explained": explained_var,
            "pca_cumulative_variance": cumulative_var
        },
        "features": features,
        "indicator_metadata": indicator_meta_export,
        "preprocessing_audit": {
            "indicator_missingness": indicator_missingness_report,
            "dropped_indicators": dropped_indicators,
            "kept_indicators": kept_indicators,
            "dropped_countries": dropped_countries_df.to_dict(orient="records"),
            "collinear_dropped": dropped_correlated,
            "imputation_stats": imputation_stats,
            "winsorize_stats": winsorize_stats,
            "correlation_matrix": {
                c1: {c2: round(float(corr_matrix_initial.loc[c1, c2]), 3) for c2 in features}
                for c1 in features
            }
        },
        "model_comparison": df_comparison.to_dict(orient="records"),
        "hierarchical_comparison": df_hierarchical.to_dict(orient="records"),
        "dendrogram_data": dendrogram_data["Ward (Euclidean)"],
        "pca": {
            "variance_explained": explained_var,
            "cumulative_variance": cumulative_var,
            "loadings": {col: [float(loadings_df.loc[col, "PC1_Loading"]), float(loadings_df.loc[col, "PC2_Loading"])] for col in features}
        },
        "cluster_profiles": cluster_profiles,
        "scaler": {
            "mean": {feat: round(float(scaler.mean_[i]), 4) for i, feat in enumerate(features)},
            "scale": {feat: round(float(scaler.scale_[i]), 4) for i, feat in enumerate(features)}
        },
        "cluster_centers": {
            cfg_id: [[round(float(val), 4) for val in center] for center in model.cluster_centers_]
            for cfg_id, model in fitted_models.items()
        },
        "countries": country_export
    }

    # Write results.json
    RESULTS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    print(f"  [SAVED] {RESULTS_JSON_PATH}")

    # Write frontend/data/results.js (window.RESULTS = ...)
    RESULTS_JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_JS_PATH, "w", encoding="utf-8") as f:
        f.write("// Autogenerated from backend/run_pipeline.py\n")
        f.write("window.RESULTS = ")
        json.dump(results_data, f, indent=2)
        f.write(";\n")
    print(f"  [SAVED] {RESULTS_JS_PATH}")

    print("\n" + "=" * 85)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Final Selection: K={selected_k} ({selected_dist.upper()}) | Silhouette: {selected_row['silhouette_euclidean']:.4f} | DB: {selected_row['davies_bouldin_euclidean']:.4f} | Stability ARI: {selected_row['stability_mean_ari']:.4f}")
    print("=" * 85)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Unsupervised Learning Clustering Pipeline")
    parser.add_argument("--data", type=str, default=None, help="Path to input dataset CSV (default: raw/nutrition_indicators.csv)")
    args = parser.parse_args()
    run_pipeline(args.data)
