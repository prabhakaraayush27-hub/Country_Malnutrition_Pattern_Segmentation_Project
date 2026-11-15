# Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![World Bank Open Data](https://img.shields.io/badge/Data-World%20Bank%20API-emerald.svg)](https://data.worldbank.org/)
[![Course: Unsupervised Learning](https://img.shields.io/badge/Course-Unsupervised%20Learning%20(CO2%2C%20CO3%2C%20CO5)-indigo.svg)](#)
[![IEEE Format Paper](https://img.shields.io/badge/Paper-IEEE%20Format-rose.svg)](docs/IEEE_RESEARCH_PAPER.md)
[![PPT Submission](https://img.shields.io/badge/PPT-15%20Nov%202026-amber.svg)](presentation/Malnutrition_Clustering_Presentation.pptx)

> **Organization:** Bill & Melinda Gates Foundation (Gates Foundation-funded Global Nutrition Report Context)  
> **Course:** Unsupervised Machine Learning (Units II, III & IV — Partition Clustering, Hierarchical Comparison, PCA Visualisation)  
> **Course Outcomes:** CO2 (Partitioning Algorithms), CO3 (Hierarchical Structuring), CO5 (Dimensionality Reduction & Projection)  
> **Submission Milestones:**  
> • **PPT Submission Deadline:** **15 November 2026** (Upload `presentation/Malnutrition_Clustering_Presentation.pptx` on UMS)  
> • **Mandatory Research Paper / Patent Deadline:** **24 November 2026** (IEEE Format Paper via Google Form)  

---

## 🔗 Project Links (Mandatory Final Deliverables)

| Resource | Description | Accessible Link |
| :--- | :--- | :--- |
| **GitHub Repository** | Complete reproducible source code, backend pipeline, frontend dashboard, and tests | [GitHub Repository Link](https://github.com/prabhakaraayush27-hub/Country_Malnutrition_Pattern_Segmentation_Project) |
| **Real World Bank Dataset** | UNICEF/WHO/World Bank Joint Malnutrition Estimates (166 Sovereign Nations × 9 Indicators) | [World Bank Open Data API](https://data.worldbank.org/indicator) • [Local Raw CSV](backend/data/raw/nutrition_indicators.csv) |
| **Live Interactive Deployment** | Production dashboard with Live What-If Simulator, PCA Explorer, and Theme Toggle | [Live Dashboard (GitHub Pages)](https://prabhakaraayush27-hub.github.io/Country_Malnutrition_Pattern_Segmentation_Project/) • [Local Live Server](http://localhost:8080/index.html) |
| **PowerPoint Presentation (PPT)** | 16:9 Widescreen Presentation (13 slides, embedded figures, project links slide) | [Malnutrition_Clustering_Presentation.pptx](presentation/Malnutrition_Clustering_Presentation.pptx) |
| **Presentation Speaker Transcript** | Slide-by-slide speaker notes, 8–10 minute timing guide, and Viva/Defense Q&A | [SLIDES_TRANSCRIPT.md](presentation/SLIDES_TRANSCRIPT.md) |
| **IEEE Research Paper (Markdown)** | Mandatory Research Paper formatted to IEEE standards (Abstract, Math, Tables, 24 Citations) | [IEEE_RESEARCH_PAPER.md](docs/IEEE_RESEARCH_PAPER.md) |
| **IEEE Research Paper (LaTeX)** | Compilable IEEEtran LaTeX document for Overleaf / Conference submission | [IEEE_RESEARCH_PAPER.tex](docs/IEEE_RESEARCH_PAPER.tex) |
| **Full Technical Report** | Comprehensive 12-section university engineering report embedding all generated figures | [REPORT.md](docs/REPORT.md) |

---

## 📌 Project Overview & Problem Statement

Malnutrition is one of the premier global health crises, yet its clinical manifestations have decoupled from simple caloric scarcity. While certain developing regions continue to experience acute child stunting and wasting, industrializing nations face surging rates of adult obesity and diet-related non-communicable diseases (NCDs). Concurrently, many developing and middle-income nations confront the **Double Burden of Malnutrition**—where chronic child undernutrition coexists with maternal and adult obesity within identical communities.

Historically, global health interventions categorized nations by macroeconomic thresholds (e.g., World Bank GNI per capita tiers). However, national income correlates imperfectly with physiological nutrition status. 

### Core Research Objective
To segment sovereign nations into objective, empirical nutritional archetypes using unsupervised machine learning applied directly to clinical and anthropometric phenotypes, isolating economic variables from feature selection to prevent circular justification.

---

## 📊 Summary of Final Results (Real World Bank Data)

- **Data Ingestion:** Ingested 217 sovereign states directly from the World Bank Open Data API (UNICEF/WHO/World Bank Joint Malnutrition Estimates and WHO/NCD-RisC surveillance series).
- **Cohort Analyzed:** 166 sovereign nations across 9 retained multidimensional health indicators after 7-step preprocessing.
- **Selected Final Model:** **Euclidean K-Means with $K = 3$** (Composite Rank #1).
  - **Silhouette Score (Common Euclidean Ruler):** `0.2726` (highest along with Manhattan K=3)
  - **Davies-Bouldin Index:** `1.7209` (well-separated clusters)
  - **Bootstrap Stability:** `0.8324 ± 0.102` ARI across 20 random 80% subsamples (exceptionally stable)
  - **Balanced Cluster Distribution:** Cluster 0 ($n=37$, 22.3%), Cluster 1 ($n=92$, 55.4%), Cluster 2 ($n=37$, 22.3%).
- **Dimensionality Reduction (PCA):** 2 components explain **65.80%** of total global nutritional variance (PC1 = 54.03%, PC2 = 11.77%).
- **Hierarchical Validation:** Ward's Linkage ($ARI = 0.7109$) and Average Linkage (Cophenetic correlation $c = 0.7427$) exhibit high concordance with K-Means at cut height **12.52**, confirming that global malnutrition naturally clusters into three distinct morphological regimes.
- **Transitional Uncertainty:** 15 borderline nations identified with silhouette scores $s < 0.05$ (e.g., Kiribati, Guatemala, Cambodia), capturing countries undergoing rapid nutritional transition along a continuum.

---

## 📁 Repository Structure

```text
Clustering project/
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages CI/CD workflow
├── presentation/                   # UMS PPT Submission (15 November 2026)
│   ├── Malnutrition_Clustering_Presentation.pptx  # 16:9 Widescreen PowerPoint Presentation
│   ├── generate_presentation.py    # Python script automating PPT generation with embedded figures
│   └── SLIDES_TRANSCRIPT.md        # Slide-by-slide speaker script, timing, & Viva Q&A prep
├── docs/                           # Academic Research Paper (24 November 2026)
│   ├── IEEE_RESEARCH_PAPER.md      # Publication-grade IEEE Research Paper (Markdown + Math)
│   ├── IEEE_RESEARCH_PAPER.tex     # Compilable IEEEtran LaTeX document for Overleaf
│   └── REPORT.md                   # Comprehensive 12-section technical engineering report
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
│   ├── run_pipeline.py                    # Master orchestrator executing 7-step pipeline & export
│   ├── make_demo_data.py                  # Offline fallback test generator (flags is_demo = True)
│   └── requirements.txt                   # Backend dependencies (numpy, pandas, scipy, sklearn, matplotlib)
├── frontend/
│   ├── css/
│   │   └── style.css                      # Luminous animated light theme + dark theme toggle
│   ├── data/
│   │   └── results.js                     # Static JS data artifact (window.RESULTS = {...})
│   ├── js/
│   │   └── app.js                         # Pure vanilla JS dashboard with Live What-If Simulator
│   ├── index.html                         # Zero-build interactive dashboard (double-click to open)
│   ├── screenshot_desktop.png             # Desktop interface capture
│   └── screenshot_mobile.png              # Mobile interface capture
├── netlify.toml                           # Netlify deployment configuration
├── .gitignore                             # Git ignore rules
└── README.md                              # Main documentation and guide
```

---

## 🔬 Mathematical & Methodological Framework

### 1. Preprocessing Pipeline (7 Controlled Steps)
1. **Indicator Missingness Filter:** Evaluated 10 candidate indicators; dropped indicators with $>40\%$ missingness (`low_birthweight` dropped; 9 retained).
2. **Country Completeness Pruning:** Dropped countries missing $>50\%$ of retained indicators (51 non-reporting microstates dropped; 166 retained).
3. **Collinearity Audit:** Pruned near-duplicate indicators ($|r| > 0.92$). Maximum correlation observed was $r = 0.88$ (`stunting` vs `underweight`). All 9 indicators retained as distinct dimensions.
4. **Hierarchical Median Imputation:** Imputed missing values using the country's geographical Region Median (Sub-Saharan Africa, Latin America, East Asia, etc.), falling back to global median.
5. **Winsorization Outlier Control:** Heavy-tailed indicators clipped at the 1st ($q_{0.01}$) and 99th ($q_{0.99}$) percentiles to prevent distortion from extreme outliers without dropping sovereign states.
6. **Categorical Profiling Isolation:** World Bank Income Group ordinal-encoded (1–4) and Region preserved as labels strictly for cluster profiling—**completely excluded from feature matrix $X$**.
7. **Z-Score Standardization:** StandardScaler applied to ensure equal variance ($\mu=0, \sigma=1$) across heterogeneous physiological measures.

### 2. Custom Manhattan K-Medians Formulation
To benchmark against standard Euclidean K-Means, a custom K-Medians algorithm was constructed in `backend/metrics.py`:
$$J_{KMedians} = \sum_{k=1}^K \sum_{x_i \in C_k} \| x_i - m_k \|_1 = \sum_{k=1}^K \sum_{x_i \in C_k} \sum_{j=1}^D |x_{ij} - m_{kj}|$$
- **Centroids:** Updated via coordinate-wise median: $m_{kj} = \text{median}(\{x_{ij} : x_i \in C_k\})$.
- **Initialization:** $L_1$-adapted $k$-means++ probability distribution with empty-cluster re-seeding.

### 3. Model Validation & Selection Criteria
- **Common Euclidean Ruler:** Evaluates all Euclidean and Manhattan models on common ground for Silhouette and Davies-Bouldin.
- **Kneedle Elbow Algorithm:** Identifies knee points in the inertia curve.
- **Bootstrap Stability Protocol:** 20 independent subsamples of 80% without replacement; records mean ARI and standard deviation.
- **Composite Rank Formula:**
  $$\text{Composite Rank} = \frac{\text{Rank}_{Sil} + \text{Rank}_{DB} + \text{Rank}_{Stab}}{3}$$
  Euclidean K-Means with $K=3$ achieves **Rank #1.0**, balancing cohesion ($s=0.2726$), separation ($DB=1.7209$), and stability ($ARI=0.8324$).

---

## 🚀 Execution & Reproducibility Guide

### 1. Prerequisites & Environment Setup
Python 3.10 or higher is required.

```powershell
# Clone repository
git clone https://github.com/prabhakaraayush27-hub/Country_Malnutrition_Pattern_Segmentation_Project.git
cd "Country_Malnutrition_Pattern_Segmentation_Project"

# Install backend dependencies
python -m pip install -r backend/requirements.txt
python -m pip install python-pptx
```

### 2. Ingest Fresh Real Data
```powershell
python backend/fetch_data.py
```
*Downloads latest data from World Bank Open Data API with automatic fallback to bulk CSV archives.*

### 3. Run Preprocessing, Clustering Sweep & Export
```powershell
python backend/run_pipeline.py
```
*Executes the 7-step preprocessing, fits all 12 partition models ($K=3..8$), runs Ward/Complete/Average hierarchical linkages, computes PCA, generates figures, and writes `frontend/data/results.js`.*

### 4. Regenerate PowerPoint Presentation
```powershell
python presentation/generate_presentation.py
```
*Builds the 13-slide 16:9 widescreen presentation with embedded figures at `presentation/Malnutrition_Clustering_Presentation.pptx`.*

### 5. Launch Interactive Dashboard Locally
```powershell
# Open directly in your web browser (zero build tools or web servers required!)
# Simply double-click frontend/index.html

# OR run local Python server
python -m http.server 8080 --directory frontend
# Navigate to: http://localhost:8080/index.html
```

---

## 🌐 Interactive Dashboard Features

1. **⚡ Live Country Nutrition Profile Simulator:**
   - 9 interactive sliders for each health indicator.
   - Real-time client-side inference using training pipeline $\mu$ and $\sigma$ ($<1\text{ms}$ calculation).
   - Instant centroid distance bars and dynamic predicted cluster badge.
   - Live projection onto PCA factor space as a pulsing glowing star marker (`★ SIMULATED NATION`).
   - Computes distance to all 166 real countries to output the **Top 3 Closest Real Sovereign States**.
   - 1-click archetype presets: *Sub-Saharan Undernutrition*, *Double Burden*, *High Obesity*, and *Low Burden*.

2. **▶ "Play Progression (K=3 to 8)" Animation Engine:**
   - Steps through cluster counts $K=3 \to 8$ on a smooth 1.6s timer to visualize cluster fracture dynamics.

3. **🔍 Interactive Country Detail Inspector Drawer:**
   - Click any scatter dot, country pill, or borderline table row to view full 9-indicator breakdown vs global averages, with a button to load that real country directly into the simulator.

4. **🎨 Luminous Animated Light Theme + Dark Theme Toggle:**
   - Flowing aurora pastel background with drifting grid and smooth theme switcher.

---

## 👥 Authors & Academic Submission

* **Author:** Abhiudhay Singh  
* **Course:** Unsupervised Machine Learning (Units II, III & IV — CO2, CO3, CO5)  
* **Organization:** Bill & Melinda Gates Foundation Nutrition Analytics Initiative  
* **PPT Submission Date:** **15 November 2026** (UMS Submission)  
* **Research Paper Submission Date:** **24 November 2026** (Google Form Submission)  
* **License:** MIT License
