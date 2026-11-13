"""
metrics.py
Clustering algorithms, distance metrics, validation scores, and hierarchical comparisons.
Implements:
  - Custom K-Medians (Manhattan L1 distance, coordinate-wise median, k-means++ L1 init, empty cluster re-seeding)
  - Common Euclidean and native metric evaluation
  - Kneedle elbow point detection
  - Bootstrap stability estimation (20 iterations, 80% subsampling, ARI)
  - Hierarchical linkage comparison (Ward, Complete, Average, Single with Euclidean & Manhattan)
  - Dendrogram coordinate extraction and cut-height calculation
  - Composite model selection ranking
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.cluster.hierarchy import linkage, cophenet, fcluster, dendrogram
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, davies_bouldin_score, adjusted_rand_score
from config import RANDOM_SEED

# ==============================================================================
# 1. Custom K-Medians Algorithm (L1 Manhattan Distance)
# ==============================================================================

class KMedians:
    """
    K-Medians clustering using Manhattan (L1) distance.
    - Centroids are coordinate-wise medians of assigned points.
    - Initialization uses K-Means++ adapted for L1 distance.
    - Handles empty clusters via furthest-point re-seeding.
    - Runs multiple restarts and retains the solution with minimum L1 inertia (WCSD).
    """
    def __init__(self, n_clusters=4, n_init=20, max_iter=300, random_state=RANDOM_SEED):
        self.n_clusters = n_clusters
        self.n_init = n_init
        self.max_iter = max_iter
        self.random_state = random_state
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None # Within-Cluster Sum of Absolute Distances (WCSD)
        
    def _init_centers_pp(self, X, rng):
        """K-means++ style initialization under L1 distance."""
        n_samples, n_features = X.shape
        centers = np.empty((self.n_clusters, n_features))
        
        # 1. Pick first center uniformly at random
        first_idx = rng.integers(0, n_samples)
        centers[0] = X[first_idx]
        
        # 2. Pick remaining centers proportional to min L1 distance
        for c in range(1, self.n_clusters):
            # Distance from each point to current centers
            dists = cdist(X, centers[:c], metric='cityblock')
            min_dists = dists.min(axis=1)
            # Avoid division by zero
            sum_d = min_dists.sum()
            if sum_d == 0:
                probs = np.ones(n_samples) / n_samples
            else:
                probs = min_dists / sum_d
            next_idx = rng.choice(n_samples, p=probs)
            centers[c] = X[next_idx]
            
        return centers

    def _fit_single_run(self, X, rng):
        """Execute a single run of K-Medians."""
        n_samples, n_features = X.shape
        centers = self._init_centers_pp(X, rng)
        labels = np.zeros(n_samples, dtype=int)
        
        for iteration in range(self.max_iter):
            # Step A: Assignment (Assign to nearest center under L1)
            dists = cdist(X, centers, metric='cityblock')
            new_labels = np.argmin(dists, axis=1)
            
            # Step B: Center update (Coordinate-wise median)
            new_centers = np.copy(centers)
            for k in range(self.n_clusters):
                cluster_mask = (new_labels == k)
                if np.any(cluster_mask):
                    new_centers[k] = np.median(X[cluster_mask], axis=0)
                else:
                    # Empty cluster re-seeding: assign the point furthest from its current center
                    current_min_dists = dists.min(axis=1)
                    furthest_idx = np.argmax(current_min_dists)
                    new_centers[k] = X[furthest_idx]
                    
            # Check convergence
            if np.array_equal(labels, new_labels):
                labels = new_labels
                centers = new_centers
                break
                
            labels = new_labels
            centers = new_centers
            
        # Compute final WCSD (inertia)
        dists = cdist(X, centers, metric='cityblock')
        min_dists = dists.min(axis=1)
        wcsd = float(np.sum(min_dists))
        
        return centers, labels, wcsd

    def fit(self, X):
        X = np.asarray(X, dtype=np.float64)
        rng = np.random.default_rng(self.random_state)
        
        best_inertia = np.inf
        best_centers = None
        best_labels = None
        
        for init_run in range(self.n_init):
            centers, labels, inertia = self._fit_single_run(X, rng)
            if inertia < best_inertia:
                best_inertia = inertia
                best_centers = centers
                best_labels = labels
                
        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        self.inertia_ = best_inertia
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=np.float64)
        dists = cdist(X, self.cluster_centers_, metric='cityblock')
        return np.argmin(dists, axis=1)

# ==============================================================================
# 2. Elbow Point Detection (Kneedle Algorithm)
# ==============================================================================

def detect_elbow_kneedle(k_values, inertias):
    """
    Detect the elbow point using the Kneedle algorithm.
    Finds the K that maximizes the perpendicular distance to the line 
    connecting the first and last points of the normalized curve.
    """
    k_arr = np.array(k_values, dtype=float)
    y_arr = np.array(inertias, dtype=float)
    
    # Normalize both axes to [0, 1]
    k_norm = (k_arr - k_arr.min()) / (k_arr.max() - k_arr.min() + 1e-12)
    y_norm = (y_arr - y_arr.min()) / (y_arr.max() - y_arr.min() + 1e-12)
    
    # Line connecting first and last normalized point: P1=(0, y_norm[0]), P2=(1, y_norm[-1])
    # Distance from point (x0, y0) to line Ax + By + C = 0
    # Line equation: (y2 - y1)*x - (x2 - x1)*y + x2*y1 - y2*x1 = 0
    p1 = np.array([k_norm[0], y_norm[0]])
    p2 = np.array([k_norm[-1], y_norm[-1]])
    
    line_vec = p2 - p1
    line_len = np.linalg.norm(line_vec)
    
    if line_len == 0:
        return k_values[0]
        
    distances = []
    for i in range(len(k_arr)):
        p0 = np.array([k_norm[i], y_norm[i]])
        # Cross product in 2D gives the perpendicular distance * line_len
        dist = np.abs(np.cross(p2 - p1, p1 - p0)) / line_len
        distances.append(dist)
        
    best_idx = int(np.argmax(distances))
    return int(k_values[best_idx])

# ==============================================================================
# 3. Bootstrap Cluster Stability Evaluation
# ==============================================================================

def compute_bootstrap_stability(X, model_class, k, n_rounds=20, subsample_ratio=0.80, random_state=RANDOM_SEED):
    """
    Compute clustering stability via bootstrap subsampling.
    Draws random 80% subsamples without replacement, fits the clustering model,
    and calculates the Adjusted Rand Index (ARI) against the full-dataset labels.
    Returns: (mean_ari, std_ari)
    """
    n_samples = X.shape[0]
    subsample_size = int(n_samples * subsample_ratio)
    rng = np.random.default_rng(random_state)
    
    # Fit full model once
    if model_class == KMeans:
        full_model = KMeans(n_clusters=k, n_init=20, random_state=random_state)
    else:
        full_model = KMedians(n_clusters=k, n_init=20, random_state=random_state)
    full_model.fit(X)
    full_labels = full_model.labels_
    
    ari_scores = []
    for b in range(n_rounds):
        sub_indices = rng.choice(n_samples, size=subsample_size, replace=False)
        X_sub = X[sub_indices]
        
        # Fit on subsample
        round_seed = rng.integers(0, 100000)
        if model_class == KMeans:
            sub_model = KMeans(n_clusters=k, n_init=10, random_state=round_seed)
        else:
            sub_model = KMedians(n_clusters=k, n_init=10, random_state=round_seed)
        sub_model.fit(X_sub)
        
        # Compare partition on the common subsample
        sub_labels = sub_model.labels_
        ref_labels = full_labels[sub_indices]
        
        score = adjusted_rand_score(ref_labels, sub_labels)
        ari_scores.append(score)
        
    return float(np.mean(ari_scores)), float(np.std(ari_scores))

# ==============================================================================
# 4. Model Sweep & Cross-Distance Common Ruler Evaluation
# ==============================================================================

def run_clustering_sweep(X, k_values, random_state=RANDOM_SEED):
    """
    Sweep across K values for both Euclidean (KMeans) and Manhattan (KMedians).
    Computes:
      - WCSS / WCSD
      - Silhouette under common Euclidean ruler AND native metric
      - Davies-Bouldin under common Euclidean ruler AND native metric
      - Bootstrap stability (mean and std ARI)
      - Cluster size distribution and min cluster size
    """
    results = []
    fitted_models = {}
    
    for distance, model_cls in [("euclidean", KMeans), ("manhattan", KMedians)]:
        for k in k_values:
            cfg_id = f"{distance}_k{k}"
            if model_cls == KMeans:
                model = KMeans(n_clusters=k, n_init=20, max_iter=300, random_state=random_state)
            else:
                model = KMedians(n_clusters=k, n_init=20, max_iter=300, random_state=random_state)
                
            model.fit(X)
            labels = model.labels_
            fitted_models[cfg_id] = model
            
            # Cluster sizes
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = {int(u): int(c) for u, c in zip(unique, counts)}
            min_cluster_size = int(min(counts)) if len(counts) > 0 else 0
            
            # Inertia / WCSS / WCSD
            # Euclidean WCSS
            wcss = float(np.sum((X - model.cluster_centers_[labels]) ** 2)) if distance == "euclidean" else float(np.sum(np.min(cdist(X, model.cluster_centers_, metric='sqeuclidean'), axis=1)))
            # Manhattan WCSD
            wcsd = float(np.sum(np.abs(X - model.cluster_centers_[labels])))
            
            # Common Euclidean Ruler Metrics
            sil_euclidean = float(silhouette_score(X, labels, metric='euclidean'))
            db_euclidean = float(davies_bouldin_score(X, labels))
            
            # Native Metric Evaluation
            if distance == "manhattan":
                sil_native = float(silhouette_score(X, labels, metric='cityblock'))
                # Custom Manhattan DB:
                # compute average within-cluster L1 distance S_i
                s_native = []
                for cl in range(k):
                    cl_pts = X[labels == cl]
                    if len(cl_pts) > 0:
                        s_native.append(np.mean(cdist(cl_pts, [model.cluster_centers_[cl]], metric='cityblock')))
                    else:
                        s_native.append(0.0)
                # compute R_ij = (S_i + S_j) / M_ij
                db_terms = []
                for i in range(k):
                    r_i = []
                    for j in range(k):
                        if i != j:
                            m_ij = np.sum(np.abs(model.cluster_centers_[i] - model.cluster_centers_[j]))
                            if m_ij > 0:
                                r_i.append((s_native[i] + s_native[j]) / m_ij)
                    if r_i:
                        db_terms.append(max(r_i))
                db_native = float(np.mean(db_terms)) if db_terms else db_euclidean
            else:
                sil_native = sil_euclidean
                db_native = db_euclidean
                
            # Bootstrap stability
            stab_mean, stab_std = compute_bootstrap_stability(
                X, model_cls, k, n_rounds=20, subsample_ratio=0.80, random_state=random_state
            )
            
            # Per-country silhouette under Euclidean
            sample_sils = silhouette_samples(X, labels, metric='euclidean')
            borderline_count = int(np.sum(sample_sils < 0.05))
            
            results.append({
                "config_id": cfg_id,
                "distance": distance,
                "k": int(k),
                "wcss": round(wcss, 3),
                "wcsd": round(wcsd, 3),
                "inertia": round(model.inertia_, 3),
                "silhouette_euclidean": round(sil_euclidean, 4),
                "davies_bouldin_euclidean": round(db_euclidean, 4),
                "silhouette_native": round(sil_native, 4),
                "davies_bouldin_native": round(db_native, 4),
                "stability_mean_ari": round(stab_mean, 4),
                "stability_std_ari": round(stab_std, 4),
                "min_cluster_size": min_cluster_size,
                "cluster_sizes": cluster_sizes,
                "borderline_count": borderline_count,
                "is_valid": bool(min_cluster_size >= 5)
            })
            
    df_results = pd.DataFrame(results)
    
    # Compute Kneedle Elbow for both distances
    kneedle_elbows = {}
    for d in ["euclidean", "manhattan"]:
        sub = df_results[df_results["distance"] == d].sort_values("k")
        val_col = "wcss" if d == "euclidean" else "wcsd"
        elbow_k = detect_elbow_kneedle(sub["k"].tolist(), sub[val_col].tolist())
        kneedle_elbows[d] = elbow_k
        
    # Composite Ranking (Only on valid models with min_cluster_size >= 5)
    valid_df = df_results[df_results["is_valid"]].copy()
    if not valid_df.empty:
        # Silhouette: higher is better (rank 1 = highest)
        valid_df["rank_sil"] = valid_df["silhouette_euclidean"].rank(ascending=False)
        # Davies-Bouldin: lower is better (rank 1 = lowest)
        valid_df["rank_db"] = valid_df["davies_bouldin_euclidean"].rank(ascending=True)
        # Stability: higher is better (rank 1 = highest)
        valid_df["rank_stab"] = valid_df["stability_mean_ari"].rank(ascending=False)
        
        valid_df["composite_score"] = (valid_df["rank_sil"] + valid_df["rank_db"] + valid_df["rank_stab"]) / 3.0
        valid_df["composite_rank"] = valid_df["composite_score"].rank(ascending=True)
        
        # Merge back ranks
        df_results = df_results.merge(
            valid_df[["config_id", "rank_sil", "rank_db", "rank_stab", "composite_score", "composite_rank"]],
            on="config_id",
            how="left"
        )
    else:
        df_results["composite_score"] = np.nan
        df_results["composite_rank"] = np.nan
        
    # Selected best model
    best_row = df_results.sort_values("composite_rank").iloc[0]
    selected_config_id = best_row["config_id"]
    
    return df_results, fitted_models, selected_config_id, kneedle_elbows

# ==============================================================================
# 5. Hierarchical Clustering Comparison
# ==============================================================================

def run_hierarchical_comparison(X, target_k, reference_labels):
    """
    Compare multiple hierarchical clustering linkages:
      - Ward (Euclidean only)
      - Complete (Euclidean & Manhattan)
      - Average (Euclidean & Manhattan)
      - Single (Euclidean)
    Computes cophenetic correlation, silhouette, DB, and ARI vs K-Means reference.
    Exports dendrogram coordinates and cut height.
    """
    linkage_configs = [
        {"name": "Ward (Euclidean)", "linkage": "ward", "metric": "euclidean"},
        {"name": "Complete (Euclidean)", "linkage": "complete", "metric": "euclidean"},
        {"name": "Average (Euclidean)", "linkage": "average", "metric": "euclidean"},
        {"name": "Single (Euclidean)", "linkage": "single", "metric": "euclidean"},
        {"name": "Complete (Manhattan)", "linkage": "complete", "metric": "cityblock"},
        {"name": "Average (Manhattan)", "linkage": "average", "metric": "cityblock"},
    ]
    
    summary = []
    linkage_matrices = {}
    dendrogram_data = {}
    
    for cfg in linkage_configs:
        metric = cfg["metric"]
        link_method = cfg["linkage"]
        
        # Pairwise distance vector
        dist_vec = pdist(X, metric=metric)
        Z = linkage(dist_vec, method=link_method)
        linkage_matrices[cfg["name"]] = Z
        
        # Cophenetic correlation
        coph_corr, _ = cophenet(Z, dist_vec)
        
        # Cut at target_k clusters
        clusters = fcluster(Z, t=target_k, criterion='maxclust') - 1 # 0-indexed
        
        # Validation scores
        sil = float(silhouette_score(X, clusters, metric='euclidean'))
        db = float(davies_bouldin_score(X, clusters))
        ari = float(adjusted_rand_score(reference_labels, clusters))
        
        # Cut height: distance threshold between target_k and target_k - 1 merges
        n_merges = Z.shape[0]
        # Merge that created target_k clusters is n_samples - target_k
        cut_idx = n_merges - (target_k - 1)
        cut_height = float(Z[cut_idx, 2]) if 0 <= cut_idx < n_merges else float(Z[-1, 2])
        
        summary.append({
            "name": cfg["name"],
            "linkage": link_method,
            "metric": metric,
            "cophenetic_correlation": round(float(coph_corr), 4),
            "silhouette": round(sil, 4),
            "davies_bouldin": round(db, 4),
            "ari_vs_kmeans": round(ari, 4),
            "cut_height": round(cut_height, 4)
        })
        
        # Extract dendrogram coordinates for visualization
        ddata = dendrogram(Z, no_plot=True, color_threshold=cut_height)
        dendrogram_data[cfg["name"]] = {
            "icoord": ddata["icoord"],
            "dcoord": ddata["dcoord"],
            "ivl": ddata["ivl"],
            "color_list": ddata["color_list"],
            "leaves": ddata["leaves"],
            "cut_height": round(cut_height, 4)
        }
        
    df_hierarchical = pd.DataFrame(summary)
    return df_hierarchical, linkage_matrices, dendrogram_data
