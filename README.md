# Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![World Bank Open Data](https://img.shields.io/badge/Data-World%20Bank%20API-emerald.svg)](https://data.worldbank.org/)
[![Course: Unsupervised Learning](https://img.shields.io/badge/Course-Unsupervised%20Learning%20(CO2%2C%20CO3%2C%20CO5)-indigo.svg)](#)

> **Organization:** Bill & Melinda Gates Foundation (Gates Foundation-funded Global Nutrition Report Context)  
> **Course:** Unsupervised Learning (Units II, III & IV — Partition Clustering, Hierarchical Comparison, PCA Visualisation)  
> **Course Outcomes:** CO2 (Partitioning Algorithms), CO3 (Hierarchical Structuring), CO5 (Dimensionality Reduction & Projection)  
> **Status:** Fully Reproducible, Real-Data Ingested, Production Frontend & Scientific Backend

---

## 📌 Project Overview & Problem Statement

Malnutrition is one of the premier global health crises, yet its clinical manifestations have decoupled from simple caloric scarcity. While certain developing regions continue to experience acute child stunting and wasting, industrializing nations face surging rates of adult obesity and diet-related non-communicable diseases (NCDs). Concurrently, many developing and middle-income nations confront the **Double Burden of Malnutrition**—where chronic child undernutrition coexists with maternal and adult obesity within identical communities.

Historically, global health interventions categorized nations by macroeconomic thresholds (e.g., World Bank GNI per capita tiers). However, national income correlates imperfectly with physiological nutrition status. 

### Core Research Objective
To segment sovereign nations into objective, empirical nutritional archetypes using unsupervised machine learning applied directly to clinical and anthropometric phenotypes, isolating economic variables from feature selection to prevent circular justification.

---

## 📊 Summary of Final Results

- **Data Ingestion:** Ingested 217 sovereign states directly from the World Bank Open Data API (UNICEF/WHO/World Bank Joint Malnutrition Estimates and WHO/NCD-RisC surveillance series).
- **Cohort Analyzed:** 166 sovereign nations across 9 retained multidimensional health indicators after 7-step preprocessing.
- **Selected Final Model:** **Euclidean K-Means with $K = 3$** (Composite Rank #1).
  - **Silhouette Score (Common Euclidean Ruler):** `0.2726` (highest along with Manhattan K=3)
  - **Davies-Bouldin Index:** `1.7209` (well-separated clusters)
  - **Bootstrap Stability:** `0.8324 ± 0.1023` ARI across 20 random 80% subsamples (exceptionally stable)
  - **Balanced Cluster Distribution:** Cluster 0 ($n=37$, 22.3%), Cluster 1 ($n=92$, 55.4%), Cluster 2 ($n=37$, 22.3%).
- **Dimensionality Reduction (PCA):** 2 components explain **65.80%** of total global nutritional variance (PC1 = 54.03%, PC2 = 11.77%).
- **Hierarchical Validation:** Ward's Linkage ($ARI = 0.7109$) and Complete Linkage ($ARI = 0.7427$) exhibit high concordance with K-Means, confirming that global malnutrition naturally clusters into three distinct morphological regimes.
- **Transitional Uncertainty:** 15 borderline nations identified with silhouette scores $s < 0.05$ (e.g., Kiribati, Guatemala, Cambodia, Gabon), capturing countries undergoing rapid nutritional transition.

---

## 📁 Repository Structure

```text
Clustering project/
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages CI/CD workflow
├── backend/
│   ├── data/
│   │   └── raw/
│   │       └── nutrition_indicators.csv  # Merged real World Bank dataset (217 x 17)
│   ├── outputs/
│   │   ├── figures/
│   │   │   ├── model_selection_panels.png # 4-panel elbow, silhouette, DB, stability curves
│   │   │   ├── pca_scatter.png            # 2D PCA projection with biplot loading vectors
│   │   │   ├── dendrogram.png             # Ward's hierarchical dendrogram at cut height 12.52
│   │   │   ├── profile_heatmap.png        # Standardized Z-score deviation heatmap
│   │   │   └── correlation_matrix.png     # 9x9 Pearson correlation matrix
│   │   ├── model_comparison.csv           # Full sweep metrics table (K=3..8, Euclidean & Manhattan)
│   │   └── results.json                   # Comprehensive pipeline output artifacts
│   ├── config.py                          # Centralized thresholds, parameters, and random seed (42)
│   ├── fetch_data.py                      # Real-world data ingestion engine with retry & fallbacks
│   ├── metrics.py                         # Custom K-Medians (L1), stability, kneedle, hierarchical tools
│   ├── run_pipeline.py                    # Master orchestrator executing 7-step pipeline & figure generation
│   ├── make_demo_data.py                  # Offline fallback test generator (flags is_demo = True)
│   └── requirements.txt                   # Backend dependencies (numpy, pandas, scipy, sklearn, matplotlib)
├── frontend/
│   ├── css/
│   │   └── style.css                      # Custom aurora glassmorphism design (Space Grotesk + Inter)
│   ├── data/
│   │   └── results.js                     # Static JS data artifact (window.RESULTS = {...})
│   ├── js/
│   │   └── app.js                         # Pure vanilla JS dashboard with responsive SVG charts
│   ├── index.html                         # Zero-build interactive dashboard (double-click to open)
│   ├── screenshot_desktop.png             # Automated headless Chrome desktop verification
│   └── screenshot_mobile.png              # Automated headless Chrome mobile verification
├── docs/
│   └── REPORT.md                          # Comprehensive university academic project report
├── .gitignore                             # Git ignore rules
├── netlify.toml                           # Netlify deployment configuration
└── README.md                              # Main documentation and guide
```

---

## 🔬 Mathematical & Methodological Framework

### 1. Preprocessing Pipeline (7 Controlled Steps)
1. **Indicator Missingness Filter:** Evaluated 10 candidate indicators; dropped indicators with $>40\%$ missingness (`low_birthweight` dropped; 9 retained).
2. **Country Completeness Pruning:** Dropped countries missing $>50\%$ of retained indicators (51 non-reporting microstates and European non-participants dropped; 166 retained).
3. **Collinearity Audit:** Pruned near-duplicate indicators ($|r| > 0.92$). Maximum correlation observed was $r = 0.88$ (`stunting` vs `underweight`). All 9 indicators retained as distinct dimensions.
4. **Hierarchical Median Imputation:** Imputed missing values using the country's geographical Region Median (Sub-Saharan Africa, Latin America, East Asia, etc.), falling back to global median.
5. **Winsorization Outlier Control:** Heavy-tailed indicators clipped at the 1st ($q_{0.01}$) and 99th ($q_{0.99}$) percentiles to prevent distortion from extreme outliers without dropping sovereign states.
6. **Categorical Profiling Isolation:** World Bank Income Group ordinal-encoded (1–4) and Region preserved as labels strictly for cluster profiling—**completely excluded from feature matrix $X$**.
7. **Z-Score Standardization:** StandardScaler applied to ensure equal variance ($\mu=0, \sigma=1$) across heterogeneous physiological measures.

### 2. Custom Manhattan K-Medians Formulation
To benchmark against standard Euclidean K-Means, a custom K-Medians algorithm was constructed in `backend/metrics.py`:
$$J_{KMedians} = \sum_{k=1}^K \sum_{x_i \in C_k} \| x_i - m_k \|_1 = \sum_{k=1}^K \sum_{x_i \in C_k} \sum_{j=1}^D |x_{ij} - m_{kj}|$$
- **Centroids:** Updated via coordinate-wise median: $m_{kj} = \text{median}(\{x_{ij} : x_i \in C_k\})$.
- **Initialization:** $L_1$ adapted k-means++ seeding ($P(x) \propto D_{L_1}(x)$).
- **Empty Cluster Re-seeding:** Data point with maximum distance to its assigned center is re-seeded as a new centroid.
- **Restarts:** 20 independent runs selecting the minimum Within-Cluster Sum of Absolute Distances (WCSD).

### 3. Common-Ruler Metric Evaluation
To compare Euclidean K-Means and Manhattan K-Medians fairly, all partitions were evaluated under a common Euclidean ruler for Silhouette and Davies-Bouldin, supplemented by native metric scores.

### 4. Bootstrap Stability Formulation
Evaluates structural reproducibility by drawing 20 independent random 80% subsamples without replacement, refitting the clustering model, and calculating the Adjusted Rand Index (ARI) against full-dataset labels:
$$\text{ARI} = \frac{\sum_{ij} \binom{n_{ij}}{2} - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{n}{2}}{\frac{1}{2} \left[ \sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2} \right] - \left[ \sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2} \right] / \binom{n}{2}}$$

---

## 🏷️ Cluster Profiles & Typological Nomenclature

Names are assigned via transparent, rule-based evaluations of the standardized undernutrition index ($Z_{under}$) and overnutrition index ($Z_{over}$):

### Cluster 0: High Undernutrition ($n = 37$, 22.3%)
- **Indices:** $Z_{under} = +1.24$, $Z_{over} = -0.91$
- **Physiological Phenotype:** Severe chronic child stunting (**33.4%**), acute wasting (**9.2%**), child underweight (**20.7%**), severe child anaemia (**61.3%**), low adult obesity (**11.4%**).
- **Demographics:** Median GDP per capita: **\$1,193**. Concentrated in Low-income (19) and Lower-middle income (18) states in Sub-Saharan Africa (Chad, Niger, Mali, Nigeria, Angola, Burundi) and South/Central Asia (Afghanistan).
- **Public Health Imperative:** Ready-to-Use Therapeutic Food (RUTF), maternal micronutrient supplementation, clean water/sanitation (WASH).

### Cluster 1: High Overweight & Obesity ($n = 92$, 55.4%)
- **Indices:** $Z_{under} = -0.63$, $Z_{over} = +0.51$
- **Physiological Phenotype:** Advanced nutritional transition: adult obesity (**29.7%**), child overweight (**8.6%**), low child stunting (**8.1%**), low child wasting (**2.7%**).
- **Demographics:** Median GDP per capita: **\$14,264**. Composed of Upper-middle (41) and High-income (40) economies in Europe & Central Asia (32), Latin America (25), Middle East/North Africa (12), North America (US, Canada).
- **Public Health Imperative:** Regulatory fiscal policies (sugar taxes, front-of-pack warning labels), metabolic syndrome screening, reformulation of processed foods.

### Cluster 2: Moderate Undernutrition / Vulnerable ($n = 37$, 22.3%)
- **Indices:** $Z_{under} = +0.32$, $Z_{over} = -0.36$
- **Physiological Phenotype:** Elevated child stunting (**22.9%**), moderate child wasting (**5.4%**), child anaemia (**42.8%**), emerging adult obesity (**18.0%**).
- **Demographics:** Median GDP per capita: **\$3,648**. Dominated by Lower-middle (18) and Upper-middle (13) income states in Sub-Saharan Africa (Ghana, Kenya, Botswana, Zimbabwe) and East Asia & Pacific (Indonesia, Philippines, Cambodia).
- **Public Health Imperative:** "Double-duty actions": promoting exclusive breastfeeding and school feeding while preventing reliance on cheap, energy-dense, nutrient-poor processed foods.

---

## 💻 How to Run Locally

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 1. Installation
Clone the repository and install required packages:
```bash
git clone <your-repository-url>
cd "Clustering project"
python -m pip install -r backend/requirements.txt
```

### 2. Ingest Fresh Real Data
Run the automated World Bank ingestion pipeline:
```bash
python backend/fetch_data.py
```
*Output: Downloads, audits, and saves real data to `backend/data/raw/nutrition_indicators.csv`.*

### 3. Execute Complete Unsupervised Pipeline
Run the preprocessing, model sweep, hierarchical benchmark, PCA projection, and figure export:
```bash
python backend/run_pipeline.py
```
*Output: Generates `backend/outputs/model_comparison.csv`, `backend/outputs/results.json`, 5 publication PNG figures, and updates `frontend/data/results.js`.*

### 4. Launch the Interactive Dashboard
The frontend requires **zero build tools, zero bundlers, and zero server runtimes**. Simply double-click `frontend/index.html` in your file explorer to open it locally, or run a lightweight Python server:
```bash
python -m http.server 8080 --directory frontend
```
Navigate to `http://localhost:8080` in your web browser.

---

## 🚀 GitHub Repository Setup & Deployment Guide

Follow these exact steps to push to GitHub and deploy the live dashboard:

### Step 1: Initialize Git Repository
In the root directory (`c:\Clustering project`):
```bash
# Initialize git
git init -b main

# Add all files (real data, code, figures, results.js)
git add .

# Create initial commit
git commit -m "feat: complete country malnutrition clustering pipeline and interactive dashboard"
```

### Step 2: Push to GitHub
Create a new public repository on GitHub (e.g. `country-malnutrition-clustering`), then link and push:
```bash
# Link your remote GitHub repository
git remote add origin https://github.com/<your-username>/country-malnutrition-clustering.git

# Push main branch
git push -u origin main
```

### Step 3: Deploy to GitHub Pages (Option A - Recommended)
1. In your GitHub repository, navigate to **Settings** > **Pages**.
2. Under **Build and deployment** > **Source**, select **GitHub Actions**.
3. The included workflow `.github/workflows/deploy.yml` will automatically build and publish the `frontend/` directory.
4. Your dashboard will be live at:
   `https://<your-username>.github.io/country-malnutrition-clustering/`

### Step 4: Deploy to Netlify (Option B)
The repository includes a ready-to-use `netlify.toml` configuring `frontend` as the publish directory with no build command needed:
1. Log in to [Netlify](https://www.netlify.com/).
2. Click **Add new site** > **Import an existing project** > **GitHub**.
3. Select your repository. Netlify detects `netlify.toml` automatically:
   - **Publish directory:** `frontend`
   - **Build command:** *(leave empty)*
4. Click **Deploy Site**.
5. Your dashboard will be live at:
   `https://<your-site-name>.netlify.app`

---

## ⚖️ Ethical Guidelines & Responsible AI Use

1. **No Country Stigmatization:** Clusters represent objective public health typologies, NOT rankings or moral evaluations. High obesity carries catastrophic cardiovascular morbidity, just as undernutrition carries high infant mortality.
2. **Strict Isolation of Economic Variables:** Gross Domestic Product (GDP) and Income Group were deliberately excluded from clustering features to prevent circular reasoning and economic determinism.
3. **Decision Support, Not Automated Decisions:** This tool is designed to support international health strategists, never to automate aid reductions or impose punitive conditionality.
4. **Continuum of Transition:** Borderline countries (such as Kiribati, Guatemala, and Cambodia) demonstrate that nutritional health exists on a continuum that transcends rigid geometric boundaries.

---

## 📜 Academic Integrity & Course Outcomes Alignment

- **Unit II (CO2 - Partition Clustering):** Implemented and compared Euclidean K-Means and custom Manhattan K-Medians with $L_1$ coordinate-wise medians and k-means++ seeding across $K \in \{3..8\}$ with 20 restarts and bootstrap stability evaluation.
- **Unit III (CO3 - Hierarchical Comparison):** Evaluated Ward, Complete, Average, and Single linkage against partition models, computing cophenetic correlation coefficients, cut heights, and Adjusted Rand Index.
- **Unit IV (CO5 - PCA Visualisation):** Reduced 9-dimensional health space to 2 principal components explaining 65.80% of total variance, interpreting factor loadings and generating biplot projection vectors.

---
*Developed for University Unsupervised Learning Coursework • Bill & Melinda Gates Foundation Nutrition Analytics Context.*
