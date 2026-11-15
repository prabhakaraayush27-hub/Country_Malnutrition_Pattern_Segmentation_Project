# Presentation Transcript & Speaker Script
## Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering
**Organization:** Bill & Melinda Gates Foundation Nutrition Analytics Initiative  
**Course:** Unsupervised Machine Learning (Units II, III & IV — CO2, CO3, CO5)  
**Submission Deadline:** 15 November 2026 (PPT Submission on UMS)  
**Presentation File:** [`presentation/Malnutrition_Clustering_Presentation.pptx`](file:///c:/Clustering%20project/presentation/Malnutrition_Clustering_Presentation.pptx)  

---

## ⏱️ Recommended Delivery Timing: 8 – 10 Minutes Total

| Slide # | Slide Title | Recommended Time | Core Objective |
| :---: | :--- | :---: | :--- |
| **1** | Title Slide | 0:30 | Establish Gates Foundation real-world context & course alignment |
| **2** | Executive Summary & Problem Statement | 1:00 | Frame the triple burden & why national averages fail |
| **3** | Real-World Data Ingestion & Audit | 0:45 | Prove empirical data authority (World Bank/UNICEF JME, 166 states) |
| **4** | 7-Step Methodological Preprocessing Pipeline | 1:00 | Walk through controlled mathematical steps and collinearity audit |
| **5** | Partition Clustering: K-Means vs K-Medians | 1:00 | Detail L2 vs L1 formulations and common Euclidean ruler |
| **6** | Hyperparameter Validation & Model Selection | 1:15 | Justify why K=3 was selected by composite rank (stability 0.8324) |
| **7** | Hierarchical Clustering Benchmark (Unit III) | 0:45 | Show Ward dendrogram cut at height 12.52 validating partition boundaries |
| **8** | 2D PCA Factor Space & Biplot Analysis (Unit IV) | 1:00 | Explain PC1 (Nutrition Transition) and PC2 (Infant Care vs Acute Stress) |
| **9** | Epidemiological Cluster Taxonomy | 1:15 | Present Cluster 0 (Undernutrition), Cluster 1 (Obesity), Cluster 2 (Transitional) |
| **10** | Borderline Cases & Sensitivity Audit | 0:45 | Discuss 15 borderline nations (silhouette < 0.05) as transition continuum |
| **11** | Interactive Decision Support & Live Simulator | 1:00 | Demonstrate live client-side inference, sliders, and PCA projection |
| **12** | Limitations & Responsible AI Ethics | 0:45 | Address survey asynchrony, ecological fallacy, and non-stigmatization |
| **13** | **Project Links (Mandatory Final Slide)** | 0:30 | Review GitHub, Dataset, Live Deployment, and IEEE Research Paper links |

---

## 🎙️ Slide-by-Slide Detailed Speaker Script

### Slide 1: Title Slide
> *"Respected Evaluators and Faculty, good day. Today I am presenting our Unsupervised Learning capstone project: **'Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering'**, developed in the context of the **Bill & Melinda Gates Foundation Nutrition Analytics Initiative**.*  
> *This work directly addresses Course Outcomes CO2, CO3, and CO5 by benchmarking partition clustering algorithms, conducting hierarchical linkage cross-validation, and projecting high-dimensional health indicators onto an interpretable 2D principal component factor space.*  
> *Importantly, every number and finding in this study is derived from **100% real World Bank Open Data** and the **UNICEF/WHO Joint Child Malnutrition Estimates** across 166 sovereign nations."*

---

### Slide 2: The Complex Real-World Malnutrition Landscape
> *"For decades, international health policy treated malnutrition as synonymous with caloric poverty. Today, the global health landscape is fundamentally more complex.*  
> *We face a **Triple Burden of Malnutrition**: first, acute child stunting and wasting concentrated in developing agrarian economies; second, surging rates of adult and child obesity driven by urbanisation and ultra-processed food markets; and third, the alarming emergence of the **'Double Burden'**, where child undernutrition and adult obesity coexist within the exact same nation or household.*  
> *Traditional economic metrics—like GDP per capita—fail to capture these physiological realities. The goal of this project is to apply unsupervised learning to uncover natural, data-driven typologies without circular economic assumptions, providing an objective decision-support framework for multilateral health funding."*

---

### Slide 3: 100% Real Empirical Health Indicators
> *"To ensure academic integrity and genuine clinical relevance, we ingested data directly from the **World Bank Open Data API**, which republishes the **UNICEF/WHO/World Bank Joint Child Malnutrition Estimates (JME)** and the **WHO/NCD-RisC** series.*  
> *Our automated ingestion pipeline queried 217 sovereign entities. We audited 10 candidate indicators: while `low_birthweight` had zero reporting records in the current reporting cycle and was dropped, 9 high-coverage indicators were successfully retained, ranging from 68.2% to 90.3% global coverage.*  
> *After excluding non-reporting microstates and dependencies with insufficient surveillance, our final clean cohort comprises **166 sovereign states** spanning every global continent."*

---

### Slide 4: 7-Step Methodological Preprocessing Pipeline
> *"A clustering algorithm is only as reliable as its preprocessing. We implemented a rigorous 7-step mathematical pipeline:*  
> 1. *First, **Missingness Filtering** (indicators missing >40% pruned).*  
> 2. *Second, **Country Completeness Filtering** (states missing >50% dropped).*  
> 3. *Third, **Multicollinearity Auditing**: we computed the pairwise Pearson correlation matrix shown on the right. Under our pre-set threshold of $|r| > 0.92$, the highest observed correlation was $r = 0.88$ between stunting and underweight. All 9 dimensions were retained as distinct features.*  
> 4. *Fourth, **Hierarchical Regional Median Imputation**: missing values were imputed using regional cohorts—such as Sub-Saharan Africa or Latin America—preserving geographical heterogeneity.*  
> 5. *Fifth, **Winsorization** at the 1st and 99th percentiles to curb extreme leverage.*  
> 6. *Sixth, a critical methodological control: **Categorical Isolation**. GDP and World Bank Income Group were kept strictly for post-clustering profiling and **never** fed to the clustering models, preventing circular reasoning.*  
> 7. *Finally, **StandardScaler Z-score Normalisation** to bring infant anthropometric percentages and adult obesity rates to zero mean and unit variance."*

---

### Slide 5: Partition Clustering: Euclidean K-Means vs. Manhattan K-Medians
> *"In Unit II, we benchmarked two distinct distance paradigms across $K \in \{3, 4, 5, 6, 7, 8\}$:*  
> *1. Standard **Euclidean K-Means**, which minimizes the $L_2$ within-cluster sum of squares inertia with 20 restarts.*  
> *2. A custom **Manhattan K-Medians** algorithm that we implemented from scratch, minimizing $L_1$ absolute deviations, calculating coordinate-wise medians as centroids, and utilizing an $L_1$-adapted k-means++ initialization with empty-cluster re-seeding.*  
> *To eliminate distance-metric bias, we benchmarked all 12 candidate configurations under a **Common Euclidean Ruler**, while simultaneously recording each model's own-metric scores.*  
> *As shown in the table, Euclidean K-Means with $K=3$ achieved the highest silhouette score (0.2726) and the highest bootstrap stability (0.8324 ARI)."*

---

### Slide 6: Hyperparameter Validation & Selection
> *"How did we select our final model? We avoided arbitrary choices by utilizing a composite ranking formula: the average of Silhouette Rank, Davies-Bouldin Rank, and 20-round Bootstrap Stability Rank.*  
> *As visualized in our model selection panels:*  
> *• The Kneedle elbow algorithm detects inertia elbows at $K=6$ (Euclidean) and $K=5$ (Manhattan).*  
> *• However, cluster stability—measured by refitting models across 20 random 80% subsamples—shows that **$K=3$ achieves exceptional reproducibility ($ARI = 0.8324 \pm 0.102$)**.*  
> *• When stepping to $K=4$, stability drops sharply to $0.5025$ ARI because countries in the transitional zone alternate between the obesity cluster and a nascent double-burden cluster.*  
> *Therefore, **Euclidean K-Means with $K=3$ emerges as the mathematically optimal macro-partition (Composite Rank #1)**."*

---

### Slide 7: Hierarchical Clustering Benchmark (Unit III)
> *"In Unit III, we verified the structural validity of our partition boundaries using Agglomerative Hierarchical Clustering across Ward, Complete, Average, and Single linkage.*  
> *As seen on the dendrogram, cutting Ward's tree at merge height **12.52** produces exactly 3 primary branches, perfectly aligning with our K-Means macro-clusters ($ARI = 0.7109$).*  
> *Average linkage achieved a **cophenetic correlation coefficient of 0.7427**, confirming that the hierarchical tree accurately reflects the true multidimensional distances. This proves that our clusters reflect natural health boundaries rather than algorithmic artifacts."*

---

### Slide 8: 2D PCA Factor Space & Biplot Analysis (Unit IV)
> *"In Unit IV, we conducted Principal Component Analysis to project the 9-dimensional health space onto 2 interpretable factor axes, capturing **65.80% of total variance**.*  
> *• **PC1 (54.03% variance)** is the **'Nutrition Transition Axis'**. It displays strong positive loadings for child stunting (+0.42), underweight (+0.42), and child anaemia (+0.38), contrasted with negative loadings for adult obesity (-0.32).*  
> *• **PC2 (11.77% variance)** represents the **'Infant Care vs. Acute Stress Axis'**, driven by exclusive breastfeeding (+0.62) vs. child wasting (-0.48).*  
> *The biplot loading vectors visually demonstrate the orthogonal nature of infant feeding practices compared to chronic growth failure."*

---

### Slide 9: Epidemiological Taxonomy of the 3 Global Clusters
> *"Using a transparent, data-driven naming rule based on standardized undernutrition and overnutrition indices ($Z_{under}, Z_{over}$), our data revealed 3 distinct global typologies:*  
> *1. **Cluster 0: High Undernutrition (37 nations, 22.3%)**: Concentrated in Sub-Saharan Africa and South Asia (Chad, Niger, Afghanistan). Stunting averages 33.4%, wasting 9.2%, anaemia 61.3%, with a median GDP of \$1,193. Immediate policy priorities are therapeutic feeding (RUTF), water/sanitation (WASH), and maternal micronutrient supplementation.*  
> *2. **Cluster 1: High Overweight & Obesity (92 nations, 55.4%)**: Dominating Europe, the Americas, and high-income states. Adult obesity reaches 29.7%, child stunting is only 8.1%, with a median GDP of \$14,264. Key policy priorities include front-of-pack warning labels, sugar-sweetened beverage taxes, and cardiometabolic screening.*  
> *3. **Cluster 2: Moderate Undernutrition / Transitional (37 nations, 22.3%)**: Encompassing emerging economies such as Ghana, Kenya, and the Philippines. Demonstrates moderate stunting (22.9%) alongside rising adult obesity (18.0%). Crucially requires **'Double-Duty Actions'** that safeguard traditional breastfeeding while curbing the aggressive penetration of ultra-processed foods."*

---

### Slide 10: Borderline Nations & Nutritional Transition
> *"A hallmark of our sensitivity audit is the identification of **15 borderline nations** with silhouette scores below $0.05$.*  
> *Countries like **Kiribati** ($s = -0.061$), **Guatemala** ($s = +0.015$), and **Cambodia** ($s = +0.007$) lie directly on cluster boundaries.*  
> *In Kiribati, for instance, a 29.8% child stunting rate coexists with a 46.0% adult obesity rate—the hallmark of the Pacific island nutrition crisis.*  
> *These borderline cases prove that nutritional transitions occur along a continuum. They caution policy makers that hard algorithmic boundaries must be interpreted with clinical flexibility."*

---

### Slide 11: Interactive Decision Support Dashboard & What-If Simulator
> *"To bridge the gap between machine learning algorithms and real-world policy, we engineered a fully interactive, static decision-support dashboard (zero build tools, vanilla HTML5/CSS3/JS):*  
> *• **Live Country Nutrition Simulator**: features 9 real-time sliders. When a user tweaks an indicator, the dashboard normalizes values using the pipeline's exact training parameters and re-computes centroid distances in less than 1 millisecond.*  
> *• **Live PCA Projection**: The simulated nation appears as a pulsing marker (`★ SIMULATED NATION`) that moves across the PCA factor space in real time.*  
> *• **Nearest Sovereign State Query**: Computes 9D Euclidean distance across all 166 nations to display the Top 3 closest real-world countries.*  
> *• **Country Inspector Drawer**: Clicking any scatter dot opens a slide-over drawer showing detailed indicator comparisons against global averages, with a button to load that real country directly into the simulator.*  
> *• **'Play Progression' Engine**: Automatically cycles $K=3$ through $K=8$ so users can observe cluster splitting dynamics."*

---

### Slide 12: Limitations, Bias Audit & Responsible AI Ethics
> *"Our project adheres to strict ethical guidelines and methodological honesty:*  
> *1. **Survey Asynchrony**: Household surveys span 2018–2023; sudden shocks (conflicts, food inflation) are subject to reporting delays.*  
> *2. **Ecological Fallacy**: National averages can mask acute subnational pockets of stunting in rural or indigenous communities.*  
> *3. **Non-Stigmatizing Nomenclature**: Clusters are defined as epidemiological typologies, not rankings or moral scorecards.*  
> *4. **Decision Support, Not Automated Conditionality**: These clusters are designed to guide holistic program design, never automate punitive aid reductions.*  
> *5. **Non-Circular Design**: Keeping GDP out of the clustering feature space prevents economic determinism from dictating health typologies."*

---

### Slide 13: Project Links & Deliverables (Mandatory Final Slide)
> *"In accordance with the submission guidelines, this final slide provides fully functional hyperlinks to all project resources:*  
> *• **GitHub Repository**: Complete source code, clean folder structure, reproducible pipeline, and comprehensive README:  
> `https://github.com/Abhiudhay-Singh/malnutrition-clustering-segmentation`*  
> *• **Real World Bank Dataset**: Verified API endpoints and raw CSV files:  
> `https://data.worldbank.org/indicator` & `backend/data/raw/nutrition_indicators.csv`*  
> *• **Live Web Deployment**: Zero-build interactive dashboard with live simulator and theme toggle:  
> `https://abhiudhay-singh.github.io/malnutrition-clustering-segmentation/` (and local live server at port 8080)*  
> *• **Academic Deliverables**:  
> - Mandatory **IEEE Research Paper** (`docs/IEEE_RESEARCH_PAPER.md` & `docs/IEEE_RESEARCH_PAPER.tex`) for the extended 24 November deadline.  
> - Full Technical Report (`docs/REPORT.md`).  
> *Thank you very much. I am now open to your questions."*

---

## ❓ Anticipated Viva / Defense Questions & Model Answers

### Q1: Why did you choose Euclidean K-Means with $K=3$ instead of $K=4$, especially when the prompt mentioned the 'Double Burden'?
> **Answer:** *"While the epidemiological concept of the double burden is clinically recognized, our composite validation metric prioritized empirical stability and cohesion. At $K=3$, our 20-round bootstrap stability is an exceptionally robust $0.8324$ ARI. At $K=4$, stability drops to $0.5025$ ARI because transitional countries alternate unstably between clusters. Rather than forcing an unstable 4-cluster model into the core report, our pipeline selected the mathematically optimal $K=3$ partition, while our interactive dashboard allows researchers to explore $K=4$ through $K=8$ and inspect how the Double Burden emerges dynamically."*

### Q2: Why did you exclude GDP per capita and Income Group from the clustering features?
> **Answer:** *"Excluding GDP was a deliberate methodological control to prevent circular reasoning and economic determinism. If GDP were included, the algorithm would cluster countries by wealth rather than by physiological nutritional state. By isolating GDP and income group strictly for post-clustering profiling, we demonstrated that health outcomes do not always correlate linearly with GDP—as evidenced by middle-income nations facing acute double-burden challenges."*

### Q3: How does your custom Manhattan K-Medians differ from standard K-Means?
> **Answer:** *"Standard K-Means minimizes $L_2$ Euclidean distance (variance), calculating arithmetic means which are sensitive to outliers. Our custom K-Medians minimizes $L_1$ absolute deviations and updates centroids using coordinate-wise medians. We also implemented $L_1$-adapted k-means++ probability seeding and empty-cluster re-seeding. In our benchmark, Euclidean K-Means achieved higher silhouette scores on our winsorized, standardized data, confirming that spherical variance minimization is optimal for this normalized feature space."*

### Q4: How does your interactive dashboard perform live predictions without a backend server?
> **Answer:** *"During the offline training run, `run_pipeline.py` exports the exact `StandardScaler` mean ($\mu$) and scale ($\sigma$) parameters, along with the 9-dimensional centroid vectors for all 12 models, into `results.js`. When a user drags a slider in the browser, client-side JavaScript standardizes the 9 inputs and computes Euclidean/Manhattan distance to each centroid in less than 1 millisecond. It then multiplies the standardized vector by the PCA loading matrix to calculate $(x_{pca}, y_{pca})$, updating the live pulsing marker on the SVG biplot instantaneously."*

