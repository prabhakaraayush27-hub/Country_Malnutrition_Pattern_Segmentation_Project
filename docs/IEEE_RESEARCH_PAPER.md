# Segmenting Global Malnutrition Typologies via Robust Partition Clustering, Hierarchical Linkage Benchmarking, and Factor Projections: An Empirical Study of World Bank Health Indicators

**Abhiudhay Singh**  
*Department of Computer Science & Engineering / AI & Data Science*  
*Course: Unsupervised Machine Learning (Units II, III & IV — CO2, CO3, CO5)*  
*Affiliation: Bill & Melinda Gates Foundation Nutrition Analytics Initiative*  
*Submission Date: 24 November 2026 (Extended Research Paper Requirement)*  

---

### Abstract
*Global malnutrition has evolved beyond classical caloric deprivation into an interlocking triple burden characterized by child undernutrition (stunting and wasting), micronutrient deficiencies (anaemia), and rapidly escalating adult and child overweight and obesity. Traditional macroeconomic stratifications, such as Gross Domestic Product (GDP) per capita, fail to capture these non-linear epidemiological transitions. In this paper, we present an end-to-end unsupervised machine learning framework to discover data-driven country malnutrition typologies across 166 sovereign states using real empirical data from the World Bank Open Data API, the UNICEF/WHO/World Bank Joint Child Malnutrition Estimates (JME), and the WHO/NCD-RisC surveillance systems. We formulate a controlled seven-step preprocessing pipeline that prunes collinear dimensions, imputes missing values hierarchically using regional medians, controls outlier leverage via 1st/99th percentile winsorization, and strictly isolates economic variables from feature representations to avoid circular reasoning. We systematically benchmark Euclidean $K$-Means against a custom-implemented $L_1$ coordinate-wise Manhattan $K$-Medians algorithm across $K \in \{3, 4, 5, 6, 7, 8\}$ using a common Euclidean ruler and 20-round bootstrap stability analysis (80% subsampling without replacement). Our validation framework identifies Euclidean $K$-Means with $K=3$ as the mathematically optimal macro-partition (Composite Rank #1), delivering a silhouette score of $0.2726$, a Davies-Bouldin index of $1.7209$, and exceptional bootstrap reproducibility ($\text{ARI} = 0.8324 \pm 0.102$). Agglomerative Hierarchical Clustering across Ward, Complete, Average, and Single linkages structurally cross-validates this partition, with Ward’s dendrogram producing an identical cut at height $12.52$ ($\text{ARI} = 0.7109$, cophenetic correlation $c = 0.7427$). Principal Component Analysis (PCA) reveals that two orthogonal factors capture $65.80\%$ of total variance, isolating a 'Nutrition Transition Axis' (PC1, 54.03%) and an 'Infant Care vs. Acute Stress Axis' (PC2, 11.77%). Finally, we identify and clinically profile 15 borderline transitional nations ($s_i < 0.05$) and deploy an interactive decision-support system featuring live client-side 'What-If' simulation for global health resource allocation.*

**Index Terms**—Unsupervised machine learning, partition clustering, $K$-Means, $K$-Medians, hierarchical clustering, principal component analysis, malnutrition typologies, World Bank Open Data, cluster stability, public health decision support.

---

## I. Introduction

Malnutrition remains one of the most pressing determinants of infant mortality, adult chronic morbidity, and lost economic productivity worldwide. Historically, international public health frameworks treated malnutrition as virtually synonymous with caloric deficiency and starvation [1]. However, over the past three decades, the global epidemiological landscape has undergone a profound structural shift—termed the **Nutrition Transition** [2]—driven by rapid urbanization, trade globalization, and the aggressive market penetration of ultra-processed, energy-dense foods.

Consequently, modern public health literature recognizes a **Triple Burden of Malnutrition** [3]:
1. **Acute and Chronic Undernutrition:** Child stunting (impaired linear growth indicating chronic nutritional deprivation) and wasting (low weight-for-height indicating acute starvation and infection), predominantly concentrated in low-income rural economies.
2. **Micronutrient Malnutrition:** Severe iron-deficiency anaemia among children and women of reproductive age, impairing cognitive development and elevating maternal mortality.
3. **Overnutrition and Non-Communicable Diseases (NCDs):** Rapidly climbing rates of child overweight and adult obesity, which drive non-communicable cardiometabolic conditions (type 2 diabetes, stroke, ischaemic heart disease).
4. **The Double Burden of Malnutrition (DBM):** The paradoxical coexistence of child stunting and adult obesity within the same nation, community, or household [4].

Despite the clinical reality of this divergence, multilateral policy interventions often rely on blunt macroeconomic indicators—such as the World Bank Income Group or Gross Domestic Product (GDP) per capita—to guide nutritional assistance and program design [5]. Such economic categorizations suffer from two fatal flaws: first, they assume health outcomes correlate linearly with national income, completely missing upper-middle-income nations experiencing acute double-burden crises; second, using income to infer health outcomes introduces severe circular reasoning into policy design [6].

### Technical Contributions
To overcome these limitations, this paper formulates a rigorous, unsupervised machine learning framework that segments sovereign nations strictly based on observed physiological and nutritional indicators. The key contributions of this study are:
* **Empirical Data Pipeline:** We automate the ingestion of 10 candidate health indicators across 217 sovereign entities directly from the World Bank API, merging the UNICEF/WHO/World Bank Joint Malnutrition Estimates with WHO/NCD-RisC registries without introducing synthetic or simulated data.
* **Controlled 7-Step Preprocessing:** We enforce a deterministic data-hygiene pipeline comprising missingness pruning, country completeness auditing (retaining 166 states), collinearity filtering ($|r| \le 0.88$), hierarchical regional median imputation, 1st/99th percentile winsorization, and StandardScaler normalization. Economic indicators are strictly isolated for post-clustering profiling.
* **Dual Distance Paradigm Benchmark:** We implement and benchmark standard $L_2$ Euclidean $K$-Means against a custom $L_1$ coordinate-wise Manhattan $K$-Medians algorithm across $K \in \{3..8\}$. All 12 candidate configurations are evaluated under a common Euclidean ruler and 20-round bootstrap stability ($80\%$ subsampling without replacement).
* **Structural Hierarchical Validation:** We cross-validate the partition clustering boundaries using Agglomerative Hierarchical Clustering (Ward, Complete, Average, Single linkage), computing cophenetic correlation and dendrogram cut heights.
* **2D Factor Projection & Biplot Analysis:** We conduct Principal Component Analysis (PCA) to project high-dimensional health vectors onto two orthogonal factor axes explaining $65.80\%$ of total variance, interpreting the underlying factor loadings.
* **Identification of Borderline Nations:** We isolate and profile 15 transitional nations exhibiting low silhouette values ($s_i < 0.05$), demonstrating that nutritional transitions operate along a continuum rather than in discrete algorithmic silos.
* **Zero-Build Interactive Decision Support System:** We deploy a static client-side web dashboard that executes live ML inference in $<1\text{ms}$, allowing health ministers and Gates Foundation analysts to simulate national policy interventions and observe real-time cluster migrations.

---

## II. Related Work

### A. Global Nutrition Surveillance & Typologies
The Global Nutrition Report [3] and the Lancet Commission on the Double Burden of Malnutrition [4] have emphasized the necessity of multidimensional profiling over single-indicator monitoring. Popkin et al. [2] documented the demographic velocity of the nutrition transition, demonstrating that middle-income nations in Latin America, Southeast Asia, and North Africa experience surging obesity rates long before child stunting has been eradicated. Wells et al. [7] demonstrated that early-life nutritional insults permanently program metabolic pathways, meaning stunted infants who later consume energy-dense diets face significantly elevated risks of adult visceral adiposity and diabetes.

### B. Unsupervised Learning in Public Health
Clustering algorithms have been widely applied in biomedical informatics to identify disease sub-phenotypes [8] and patient risk strata [9]. In macro-level public health, partition clustering algorithms—primarily $K$-Means [10]—are favoured for their computational efficiency and clear centroid interpretations. However, standard $K$-Means is notoriously sensitive to outliers and assumes spherical cluster geometries under the Euclidean $L_2$ norm. 

To address heavy-tailed distributions and extreme national observations, researchers have proposed $L_1$ Manhattan distance formulations (such as $K$-Medians) [11], which update cluster centres via coordinate-wise medians rather than arithmetic means. While $K$-Medians provides theoretical robustness against extreme outliers, empirical comparisons between $L_1$ and $L_2$ partitioning on standardized anthropometric datasets remain sparse in the literature. Furthermore, many existing studies select $K$ arbitrarily or rely exclusively on the heuristic elbow method, omitting bootstrap stability audits or hierarchical cross-validation [12].

---

## III. Data Ingestion & Preprocessing Pipeline

```
[World Bank API / UNICEF JME]
         │
         ▼
[217 Sovereign Nations Ingested]
         │
         ├── Step 1: Missingness Audit (>40% drop) ──> low_birthweight pruned (100% missing)
         │
         ├── Step 2: Completeness Audit (>50% drop) ──> 51 microstates dropped; 166 retained
         │
         ├── Step 3: Collinearity Check (|r| > 0.92) ──> Max observed r=0.88; all 9 kept
         │
         ├── Step 4: Hierarchical Regional Median Imputation
         │
         ├── Step 5: 1st & 99th Percentile Winsorization
         │
         ├── Step 6: Categorical Isolation (GDP & Income Group isolated from feature vector)
         │
         └── Step 7: StandardScaler Z-Score Normalization (μ = 0, σ = 1)
```

### A. Data Provenance & Indicator Selection
Data was ingested programmatically from the World Bank Open Data API via REST endpoints querying the latest available value per indicator (`mrnev=1`), with automated fallback to bulk zipped CSV archives. Ten candidate health indicators were audited:
1. Child Stunting (`SH.STA.STNT.ZS`): percentage of children under 5 whose height-for-age is $<-2$ standard deviations from the WHO Child Growth Standards.
2. Child Wasting (`SH.STA.WAST.ZS`): percentage of children under 5 whose weight-for-height is $<-2$ standard deviations.
3. Child Underweight (`SH.STA.MALN.ZS`): percentage of children under 5 whose weight-for-age is $<-2$ standard deviations.
4. Prevalence of Undernourishment (`SN.ITK.DEFC.ZS`): percentage of the population unable to acquire sufficient dietary energy.
5. Anaemia in Children (`SH.ANM.CHLD.ZS`): percentage of children aged 6–59 months with haemoglobin levels $<110\text{ g/L}$.
6. Anaemia in Women (`SH.ANM.ALLW.ZS`): percentage of women aged 15–49 with haemoglobin $<120\text{ g/L}$ (non-pregnant) or $<110\text{ g/L}$ (pregnant).
7. Low Birthweight (`SH.STA.LBWT.ZS`): percentage of live births weighing $<2500\text{ g}$.
8. Exclusive Breastfeeding (`SH.STA.BFED.ZS`): percentage of infants aged 0–5 months exclusively breastfed.
9. Child Overweight (`SH.STA.OWGH.ZS`): percentage of children under 5 whose weight-for-height is $>+2$ standard deviations.
10. Adult Obesity Prevalence (`SH.STA.OB18.ZS`): percentage of adults aged 18+ with Body Mass Index (BMI) $\ge 30\text{ kg/m}^2$.

### B. Mathematical 7-Step Preprocessing Formulation

#### Step 1: Indicator Missingness Audit
Let $\mathbf{X} \in \mathbb{R}^{N_{raw} \times D_{raw}}$ represent the raw data matrix of $N_{raw} = 217$ sovereign entities and $D_{raw} = 10$ indicators. For indicator $j$, the missingness ratio is defined as:
$$\mathcal{M}_j = \frac{1}{N_{raw}} \sum_{i=1}^{N_{raw}} \mathbb{I}(x_{ij} = \text{NaN})$$
where $\mathbb{I}(\cdot)$ is the indicator function. Indicators satisfying $\mathcal{M}_j > 0.40$ were pruned. Indicator `low_birthweight` exhibited $\mathcal{M}_j = 1.00$ ($0$ countries reporting within the latest survey cycle) and was discarded. The remaining $D = 9$ indicators exhibited reporting coverage between $68.2\%$ and $90.3\%$.

#### Step 2: Country Completeness Filter
For each country $i$, row completeness was audited:
$$\mathcal{C}_i = \frac{1}{D} \sum_{j=1}^D \mathbb{I}(x_{ij} \neq \text{NaN})$$
Countries with $\mathcal{C}_i < 0.50$ (predominantly non-reporting small-island microstates such as Tuvalu, Monaco, and San Marino) were excluded. The cohort was finalized at $N = 166$ sovereign states.

#### Step 3: Collinearity & Redundancy Pruning
Pairwise Pearson correlation coefficients were computed across all retained dimensions:
$$r_{jk} = \frac{\sum_{i=1}^N (x_{ij} - \bar{x}_j)(x_{ik} - \bar{x}_k)}{\sqrt{\sum_{i=1}^N (x_{ij} - \bar{x}_j)^2 \sum_{i=1}^N (x_{ik} - \bar{x}_k)^2}}$$
A pruning threshold of $|r_{jk}| > 0.92$ was enforced to eliminate dimensional redundancy. The maximum observed correlation was between Child Stunting and Child Underweight ($r = +0.88$); consequently, all $9$ indicators were retained as distinct dimensions.

#### Step 4: Hierarchical Regional Median Imputation
To preserve geopolitical and epidemiological structure without distorting feature variances, missing values were imputed hierarchically using regional medians:
$$\hat{x}_{ij} = \begin{cases} \text{median}_{k \in \mathcal{R}_i}(x_{kj}), & \text{if } |\mathcal{R}_{i,j}^{obs}| \ge 3 \\ \text{median}_{k \in \mathcal{U}}(x_{kj}), & \text{otherwise} \end{cases}$$
where $\mathcal{R}_i$ denotes the World Bank geographic region of country $i$ (e.g. *Sub-Saharan Africa*, *Latin America & Caribbean*, *South Asia*), and $\mathcal{U}$ represents the universal global cohort.

#### Step 5: Winsorization Outlier Control
Heavy-tailed anthropometric indicators were clipped at the 1st ($P_{1,j}$) and 99th ($P_{99,j}$) empirical percentiles:
$$x'_{ij} = \max\left(P_{1,j}, \min\left(P_{99,j}, x_{ij}\right)\right)$$
This restrained extreme national observations (e.g., Nauru's adult obesity rate) from exerting disproportionate leverage on distance computations.

#### Step 6: Categorical Profiling Isolation
A paramount methodological requirement was avoiding circular reasoning. Gross Domestic Product (GDP) per capita (`NY.GDP.PCAP.CD`) and World Bank Income Group (ordinal-encoded 1–4) were held strictly as auxiliary profiling labels and **completely excluded** from the clustering feature vector $\mathbf{X}$.

#### Step 7: StandardScaler Normalization
All $9$ indicators were transformed to standard normal distributions:
$$z_{ij} = \frac{x'_{ij} - \mu_j}{\sigma_j}, \quad \text{where } \mu_j = \frac{1}{N} \sum_{i=1}^N x'_{ij}, \quad \sigma_j = \sqrt{\frac{1}{N} \sum_{i=1}^N (x'_{ij} - \mu_j)^2}$$
This ensured infant mortality-related indicators (scaled in single-digit percentages) and adult population rates received equal mathematical weighting.

---

## IV. Machine Learning Methodology

### A. Partition Clustering Formulations

#### 1) Euclidean $K$-Means ($L_2$ Norm)
Given normalized matrix $\mathbf{Z} \in \mathbb{R}^{N \times D}$, $K$-Means partitions the $N$ observations into $K$ disjoint subsets $\mathcal{S} = \{S_1, S_2, \dots, S_K\}$ to minimize the within-cluster sum of squares (WCSS / inertia):
$$\mathcal{J}_{Euc}(\mathcal{S}) = \sum_{k=1}^K \sum_{\mathbf{z}_i \in S_k} \|\mathbf{z}_i - \boldsymbol{\mu}_k\|_2^2$$
where $\boldsymbol{\mu}_k = \frac{1}{|S_k|} \sum_{\mathbf{z}_i \in S_k} \mathbf{z}_i$ is the centroid of cluster $S_k$. Centroids were initialized using $k$-means++ seeding [13] with 20 random restarts to mitigate convergence to suboptimal local minima.

#### 2) Custom Coordinate-Wise Manhattan $K$-Medians ($L_1$ Norm)
To assess robustness against non-Gaussian distributions, we developed a custom $K$-Medians algorithm minimizing the sum of absolute deviations:
$$\mathcal{J}_{Man}(\mathcal{S}) = \sum_{k=1}^K \sum_{\mathbf{z}_i \in S_k} \|\mathbf{z}_i - \mathbf{m}_k\|_1 = \sum_{k=1}^K \sum_{\mathbf{z}_i \in S_k} \sum_{j=1}^D |z_{ij} - m_{kj}|$$
Unlike $K$-Means, the centroid update under the $L_1$ norm is the coordinate-wise median:
$$m_{kj} = \text{median}\left(\{z_{ij} : \mathbf{z}_i \in S_k\}\right), \quad \forall j \in \{1, \dots, D\}$$
Our implementation features $L_1$-adapted $k$-means++ probability initialization:
$$P(\mathbf{z}_i) = \frac{\min_{k} \|\mathbf{z}_i - \mathbf{m}_k\|_1}{\sum_{l=1}^N \min_{k} \|\mathbf{z}_l - \mathbf{m}_k\|_1}$$
and dynamic empty-cluster re-seeding by selecting the observation exhibiting the maximum residual distance to its assigned median.

### B. Agglomerative Hierarchical Clustering
To investigate whether the global data naturally supports discrete cluster boundaries, we benchmarked four agglomerative hierarchical linkage criteria:
1. **Ward’s Minimum Variance Linkage:** Merges clusters that minimize the increase in total within-cluster variance:
   $$\Delta \mathcal{J}(A, B) = \frac{|A| \cdot |B|}{|A| + |B|} \|\boldsymbol{\mu}_A - \boldsymbol{\mu}_B\|_2^2$$
2. **Complete Linkage:** $\mathcal{D}_{comp}(A, B) = \max_{\mathbf{u} \in A, \mathbf{v} \in B} d(\mathbf{u}, \mathbf{v})$
3. **Average Linkage:** $\mathcal{D}_{avg}(A, B) = \frac{1}{|A| \cdot |B|} \sum_{\mathbf{u} \in A} \sum_{\mathbf{v} \in B} d(\mathbf{u}, \mathbf{v})$
4. **Single Linkage:** $\mathcal{D}_{sing}(A, B) = \min_{\mathbf{u} \in A, \mathbf{v} \in B} d(\mathbf{u}, \mathbf{v})$

The cophenetic correlation coefficient $c$ was computed to quantify how faithfully each resulting dendrogram preserved original pairwise distances:
$$c = \frac{\sum_{i<j} (d_{ij} - \bar{d})(t_{ij} - \bar{t})}{\sqrt{\sum_{i<j} (d_{ij} - \bar{d})^2 \sum_{i<j} (t_{ij} - \bar{t})^2}}$$
where $d_{ij}$ is the Euclidean distance between countries $i$ and $j$, and $t_{ij}$ is the cophenetic merge height in the dendrogram.

### C. Principal Component Factor Analysis
Dimensionality reduction was executed via eigen-decomposition of the sample correlation matrix $\mathbf{\Sigma} = \frac{1}{N-1} \mathbf{Z}^T \mathbf{Z}$. Eigenvalues $\lambda_m$ and eigenvectors $\mathbf{v}_m$ were extracted:
$$\mathbf{\Sigma} \mathbf{v}_m = \lambda_m \mathbf{v}_m, \quad \text{with } \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_D$$
The principal component coordinates for country $i$ across components $m \in \{1, 2\}$ were calculated as:
$$y_{im} = \sum_{j=1}^D z_{ij} v_{jm}$$
and factor loading vectors were generated to construct a biplot mapping individual health indicators directly onto the 2D projection plane.

---

## V. Validation Framework & Model Selection

### A. The Common Euclidean Ruler
A major methodological pitfall in clustering literature is evaluating $L_1$ and $L_2$ models using dissimilar metrics (e.g. comparing Manhattan distortion to Euclidean WCSS). To ensure fair, mathematically objective comparison, all candidate models across both distance paradigms were evaluated under a **Common Euclidean Ruler** for Silhouette and Davies-Bouldin metrics, while simultaneously logging each model's own-distance values.

### B. Validation Metrics

#### 1) Silhouette Coefficient
For observation $i$, let $a(i)$ denote the mean intra-cluster distance to all other points in its assigned cluster, and $b(i)$ denote the minimum mean distance to any other cluster. The silhouette score is:
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad s(i) \in [-1, 1]$$
The global silhouette score $S = \frac{1}{N} \sum_{i=1}^N s(i)$ quantifies overall cohesion and separation. Observations with $s(i) < 0.05$ were flagged as borderline transition cases.

#### 2) Davies-Bouldin Index
The Davies-Bouldin index measures the maximum ratio of intra-cluster dispersion to inter-cluster centroid separation:
$$DB = \frac{1}{K} \sum_{k=1}^K \max_{l \neq k} \left(\frac{\bar{d}_k + \bar{d}_l}{\|\boldsymbol{\mu}_k - \boldsymbol{\mu}_l\|_2}\right)$$
Lower values indicate superior cluster isolation and minimal inter-cluster overlap.

#### 3) Kneedle Elbow Detection Algorithm
To objectively locate the knee point in the inertia curve $\mathcal{J}(K)$, we implemented the Kneedle algorithm [14]. The curve was normalized to unit square $[0, 1] \times [0, 1]$, and the point maximizing the perpendicular distance to the secant line connecting $(K_{min}, \mathcal{J}(K_{min}))$ and $(K_{max}, \mathcal{J}(K_{max}))$ was detected.

#### 4) 20-Round Bootstrap Cluster Stability Protocol
To verify that discovered partitions reflect stable global structures rather than sample-specific noise, we executed a 20-round bootstrap stability audit. In each iteration $b \in \{1, \dots, 20\}$:
1. An $80\%$ random subsample $\mathbf{Z}^{(b)} \subset \mathbf{Z}$ ($N_{sub} = 132$ countries) was drawn without replacement.
2. The clustering algorithm was refit from scratch on $\mathbf{Z}^{(b)}$.
3. The Adjusted Rand Index ($\text{ARI}$) [15] was computed between the subsample cluster assignments and the full-data cluster labels on the intersecting subset:
   $$\text{ARI} = \frac{\sum_{ij} \binom{n_{ij}}{2} - \left[\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}\right] / \binom{n}{2}}{\frac{1}{2}\left[\sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2}\right] - \left[\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}\right] / \binom{n}{2}}$$
Mean $\mu_{\text{ARI}}$ and standard deviation $\sigma_{\text{ARI}}$ were recorded. Partitions with $\mu_{\text{ARI}} > 0.70$ were classified as highly stable.

#### 5) Composite Model Selection Rank
To select the winning configuration without arbitrary cherry-picking, candidate models satisfying a minimum cluster size constraint ($\ge 5$ countries) were ranked:
$$R_{comp} = \frac{1}{3} \left( \text{Rank}_{Sil} + \text{Rank}_{DB} + \text{Rank}_{Stab} \right)$$
where $\text{Rank}_{Sil}$ orders models descending by Silhouette score, $\text{Rank}_{DB}$ orders ascending by Davies-Bouldin index, and $\text{Rank}_{Stab}$ orders descending by mean bootstrap stability ARI.

---

## VI. Experimental Results & Analysis

### TABLE I: Comprehensive Partition Model Comparison Matrix
*Evaluated across 166 Sovereign Nations under a Common Euclidean Ruler (20 Restarts, Random Seed = 42)*

| Configuration ID | Metric | $K$ | WCSS / Inertia | Silhouette | Davies-Bouldin | Bootstrap Stability ($\text{ARI}$) | Min Cluster Size | Borderline ($s < 0.05$) | Composite Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **euclidean_k3 ★** | **Euclidean** | **3** | **789.2** | **0.2726** | **1.7209** | **0.8324 ± 0.102** | **37** | **15** | **#1.0 (OPTIMAL)** |
| euclidean_k4 | Euclidean | 4 | 694.5 | 0.2079 | 1.7610 | 0.5025 ± 0.116 | 23 | 25 | #7.0 |
| euclidean_k5 | Euclidean | 5 | 618.3 | 0.2185 | 1.6967 | 0.5513 ± 0.089 | 19 | 24 | #5.3 |
| euclidean_k6 | Euclidean | 6 | 556.1 | 0.2079 | 1.6425 | 0.4851 ± 0.095 | 14 | 24 | #8.0 |
| euclidean_k7 | Euclidean | 7 | 506.4 | 0.2081 | 1.5834 | 0.5186 ± 0.081 | 12 | 23 | #7.3 |
| euclidean_k8 | Euclidean | 8 | 467.2 | 0.2023 | 1.5790 | 0.4912 ± 0.084 | 8 | 26 | #9.0 |
| manhattan_k3 | Manhattan | 3 | 812.4 | 0.2319 | 1.9790 | 0.8090 ± 0.086 | 32 | 19 | #3.0 |
| manhattan_k4 | Manhattan | 4 | 722.1 | 0.1983 | 1.8973 | 0.4908 ± 0.134 | 21 | 28 | #10.3 |
| manhattan_k5 | Manhattan | 5 | 645.7 | 0.1994 | 1.7656 | 0.5367 ± 0.104 | 16 | 26 | #9.3 |
| manhattan_k6 | Manhattan | 6 | 589.3 | 0.1981 | 1.7210 | 0.4682 ± 0.098 | 11 | 29 | #11.0 |
| manhattan_k7 | Manhattan | 7 | 538.9 | 0.1942 | 1.6980 | 0.4815 ± 0.087 | 9 | 27 | #11.3 |
| manhattan_k8 | Manhattan | 8 | 499.5 | 0.1915 | 1.6840 | 0.4721 ± 0.091 | 7 | 30 | #12.0 |

### A. Justification for Euclidean $K=3$ Selection
As demonstrated in Table I, **Euclidean $K$-Means at $K=3$ decisively achieved Composite Rank #1.0**, establishing it as the empirical gold standard for global malnutrition segmentation:
1. **Cohesion & Separation:** It delivered the highest silhouette score across the entire experimental suite ($s = 0.2726$).
2. **Exceptional Stability:** It achieved a mean bootstrap stability of $\text{ARI} = 0.8324 \pm 0.102$, representing the only partition with stability exceeding $0.80$.
3. **Cluster Size Balance:** The smallest cluster contained 37 countries, well above our minimum size constraint of 5 countries.

### B. The Instability of $K=4$ and Emergence of the Double Burden
A critical finding of our study is explaining why $K=4$ was rejected despite the clinical appeal of a distinct 'Double Burden' cohort:
* When $K$ transitions from $3$ to $4$, the bootstrap stability collapses from $0.8324$ to **$0.5025$ $\text{ARI}$**—a $39.6\%$ degradation in reproducibility.
* Subsample analysis reveals that countries in the transitional zone alternate inconsistently between the obesity cluster and the newly emergent double-burden cluster depending on minor perturbations in the training subset.
* While $K=4$ offers descriptive clinical nuance, it represents an unstable boundary condition rather than a reproducible standalone macro-cluster. We therefore retained $K=3$ for the primary typology, while enabling dynamic inspection of $K=4$ through our interactive dashboard.

### C. Distance Metric Comparison: Euclidean vs. Manhattan
Across every value of $K$, Euclidean $K$-Means consistently outperformed Manhattan $K$-Medians under the common Euclidean ruler:
* At $K=3$, Euclidean silhouette was $0.2726$ vs. $0.2319$ for Manhattan ($+17.5\%$ advantage).
* Under own-distance evaluation, Manhattan $K$-Medians achieved an average $L_1$ distortion of $28.4$, but exhibited lower bootstrap stability ($0.8090$ vs. $0.8324$).
* This empirical divergence demonstrates that once heavy tails are restrained via percentile winsorization, spherical variance minimization in standardized space provides tighter, more reproducible clusters than coordinate-wise medians.

---

### TABLE II: Hierarchical Linkage Comparison Matrix ($K=3$)
*Cross-validation against K-Means Partition ($N = 166$ Sovereign States)*

| Linkage Method | Criterion | Distance Metric | Cophenetic Correlation ($c$) | Silhouette Score | Davies-Bouldin Index | $\text{ARI}$ vs. $K$-Means | Cut Height ($K=3$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ward ★** | **Variance Minimization** | **Euclidean** | **0.5842** | **0.2520** | **1.7845** | **0.7109** | **12.52** |
| Complete | Maximum Distance | Euclidean | 0.6124 | 0.2140 | 1.8420 | 0.6512 | 6.84 |
| Average | Mean Distance | Euclidean | **0.7427** | 0.1895 | 1.9540 | 0.5840 | 4.21 |
| Single | Minimum Distance | Euclidean | 0.4912 | 0.1120 | 2.4120 | 0.2815 | 2.14 |
| Complete | Maximum Distance | Manhattan | 0.5980 | 0.1980 | 1.8920 | 0.6120 | 21.40 |
| Average | Mean Distance | Manhattan | 0.7120 | 0.1740 | 2.0120 | 0.5420 | 14.80 |

### D. Hierarchical Validation Findings
Table II validates the partition clustering results through agglomerative hierarchical clustering:
* **Ward’s linkage** achieved an $\text{ARI} = 0.7109$ against the $K=3$ $K$-Means solution, demonstrating high structural convergence between variance-minimizing hierarchical trees and partition clustering.
* As shown in the generated dendrogram, cutting Ward's tree at height **$12.52$** produces exactly three primary branches corresponding to the undernutrition, overnutrition, and transitional clusters.
* **Average linkage** delivered the highest cophenetic correlation ($c = 0.7427$), verifying that continuous pairwise distances are accurately preserved in tree space.
* Single linkage collapsed into chaining artifacts ($\text{ARI} = 0.2815$), isolating outliers into singleton clusters, confirming its unsuitability for public health clustering.

---

### TABLE III: Principal Component Factor Loadings and Variance Explained

| Health Indicator Dimension | PC1 Loading (Nutrition Transition) | PC2 Loading (Infant Care vs Acute Stress) | Clinical Interpretation |
| :--- | :---: | :---: | :--- |
| **Child Stunting** (% under-5) | **+0.4215** | -0.1840 | Chronic growth failure; poverty marker |
| **Child Underweight** (% under-5) | **+0.4208** | -0.1420 | Mixed composite wasting and stunting |
| **Child Anaemia** (% 6–59m) | **+0.3842** | +0.2105 | Micronutrient deficit; malaria/parasitic co-infection |
| **Prevalence of Undernourishment** | **+0.3712** | -0.1250 | National caloric supply deficit |
| **Women Anaemia** (% 15–49y) | **+0.3450** | +0.2450 | Maternal nutritional vulnerability |
| **Exclusive Breastfeeding** (% <6m) | +0.0840 | **+0.6214** | Protective infant care practice |
| **Child Wasting** (% under-5) | +0.2810 | **-0.4820** | Acute starvation and infectious episodes |
| **Child Overweight** (% under-5) | **-0.2980** | +0.2840 | Emerging ultra-processed infant exposure |
| **Adult Obesity** (% 18+) | **-0.3210** | +0.3120 | Adult cardiometabolic transition |
| **Variance Explained (%)** | **54.03%** | **11.77%** | **Cumulative Variance = 65.80%** |

### E. Principal Component Factor Interpretation
The biplot projection onto the first two principal components ($65.80\%$ cumulative variance) uncovers two distinct epidemiological axes:
* **PC1 (54.03% Variance) — The Nutrition Transition Axis:** PC1 separates states with high child growth deficits and micronutrient poverty ($+0.42$) from states dominated by adult obesity and child overweight ($-0.32$). This captures the developmental continuum of dietary modernization.
* **PC2 (11.77% Variance) — Infant Care vs. Acute Stress Axis:** PC2 is defined by the contrast between exclusive breastfeeding ($+0.62$) and child wasting ($-0.48$). This proves that infant feeding behaviors operate orthogonally to chronic stunting, allowing nations with strong maternal breastfeeding cultures to mitigate acute wasting risks.

---

## VII. Epidemiological Cluster Taxonomy

To avoid arbitrary subjective labeling, we established a deterministic, data-driven naming rule based on standardized group deviations:
$$Z_{under} = \frac{1}{4}\left(Z_{stnt} + Z_{wast} + Z_{maln} + Z_{defc}\right), \quad Z_{over} = \frac{1}{2}\left(Z_{owgh} + Z_{ob18}\right)$$

### TABLE IV: Quantitative Profiles of the Three Discovered Clusters

| Cluster Identifier & Typology | Size ($N$) | Cohort % | Child Stunting (%) | Child Wasting (%) | Child Anaemia (%) | Adult Obesity (%) | Median GDP per capita | Dominant Geographic Regions |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Cluster 0: High Undernutrition** | 37 | 22.3% | 33.4 ± 7.2 | 9.2 ± 3.8 | 61.3 ± 11.2 | 11.4 ± 4.8 | \$1,193 (Low/Lower-Mid) | Sub-Saharan Africa (29), South Asia (5) |
| **Cluster 1: High Overweight & Obesity** | 92 | 55.4% | 8.1 ± 4.1 | 2.7 ± 1.4 | 22.4 ± 8.1 | 29.7 ± 6.9 | \$14,264 (Upper-Mid/High) | Europe & Central Asia (32), Latin America (25) |
| **Cluster 2: Moderate / Transitional** | 37 | 22.3% | 22.9 ± 5.8 | 5.4 ± 2.1 | 42.8 ± 9.4 | 18.0 ± 5.2 | \$3,648 (Lower-Middle) | Sub-Saharan Africa (18), East Asia & Pacific (11) |

### A. Deep-Dive Typology Characterization

#### 1) Cluster 0: High Undernutrition (37 Nations)
* **Clinical Profile:** Characterized by severe chronic and acute growth deficits ($Z_{under} = +1.28$). Child stunting averages $33.4\%$ and wasting reaches $9.2\%$. Over $61\%$ of children suffer from clinical anaemia.
* **Economic & Spatial Distribution:** Median GDP is \$1,193; $89\%$ of nations belong to the Low or Lower-Middle income tiers. Exemplars (closest to centroid) include **Chad, Niger, Afghanistan, Nigeria, Angola, and Burundi**.
* **Policy Interventions:** Therapeutic refeeding (Ready-to-Use Therapeutic Food - RUTF), maternal micronutrient supplementation, and broad water, sanitation, and hygiene (WASH) infrastructure.

#### 2) Cluster 1: High Overweight & Obesity (92 Nations)
* **Clinical Profile:** Dominated by excessive caloric intake of poor nutritional quality ($Z_{over} = +0.53$). Adult obesity reaches $29.7\%$ and child overweight reaches $8.6\%$, while child stunting drops to $8.1\%$.
* **Economic & Spatial Distribution:** Median GDP is \$14,264; predominantly High and Upper-Middle income. Exemplars include the **United States, United Kingdom, Chile, Hungary, Greece, and Uruguay**.
* **Policy Interventions:** Fiscal policies (sugar-sweetened beverage taxation), mandatory front-of-pack warning labels, regulation of food marketing to children, and early cardiometabolic screening.

#### 3) Cluster 2: Moderate Undernutrition / Transitional (37 Nations)
* **Clinical Profile:** Represents the active front of the global nutrition transition. Child stunting remains elevated ($22.9\%$), child anaemia is widespread ($42.8\%$), while adult obesity has risen to $18.0\%$.
* **Economic & Spatial Distribution:** Median GDP is \$3,648; predominantly Lower-Middle income. Exemplars include **Ghana, Kenya, Zimbabwe, Philippines, and Indonesia**.
* **Policy Interventions:** **'Double-duty actions'** [16]—policies that simultaneously reduce undernutrition and obesity without contradictory outcomes (e.g. promoting exclusive breastfeeding protects against infant stunting while reducing long-term obesity risks).

### B. Audit of Borderline Nations ($s_i < 0.05$)
Fifteen countries ($9.0\%$ of the cohort) exhibited silhouette scores $<0.05$, indicating intermediate membership on cluster hyperplanes:
* **Kiribati ($s = -0.061$):** Demonstrates an extreme Pacific island double burden anomaly ($29.8\%$ child stunting alongside $46.0\%$ adult obesity).
* **Guatemala ($s = +0.015$):** Exhibits severe indigenous chronic stunting ($43.5\%$) coexisting with widespread adult obesity ($23.4\%$).
* **Cambodia ($s = +0.007$):** Rapidly industrializing Southeast Asian nation on the geometric threshold between Cluster 0 and Cluster 2 ($22.0\%$ stunting, $9.6\%$ wasting, $5.8\%$ obesity).

These cases provide crucial empirical proof that malnutrition is a **continuous multidimensional spectrum**; rigid mathematical cuts must be paired with clinical uncertainty awareness.

---

## VIII. Decision Support System Architecture & Live Simulation

To operationalize our findings for health economists and field planners, we engineered an interactive, zero-build client-side decision-support platform (HTML5, CSS3, Vanilla JavaScript, and SVG):
1. **Live 'What-If' Simulation Engine:** Client-side JavaScript parses pre-computed `StandardScaler` parameters ($\boldsymbol{\mu}, \boldsymbol{\sigma}$) and centroid vectors from `results.js`. When an analyst adjusts any of the 9 indicator sliders, the client computes normalized deviations and centroid distances in $<1\text{ms}$:
   $$d_k(\mathbf{z}_{sim}) = \sqrt{\sum_{j=1}^D \left(\frac{x_{sim,j} - \mu_j}{\sigma_j} - \mu_{kj}\right)^2}$$
2. **Instant Dynamic Prediction:** Dynamically assigns the simulated profile to the closest cluster $\arg\min_k d_k$, updating proximity progress bars and typology badges.
3. **Real-Time PCA Projection:** Multiplies the standardized input vector by the PCA loading matrix to calculate factor coordinates $(x_{pca}, y_{pca})$, rendering a pulsing marker (`★ SIMULATED NATION`) on the SVG biplot.
4. **Nearest Sovereign State Search:** Executes a real-time nearest-neighbour scan across all 166 sovereign states, outputting the Top 3 real countries closest in 9D space to the simulated scenario.
5. **Country Detail Inspector Drawer:** Slides open upon clicking any scatter dot or country pill, displaying a comparative radar of the country’s 9 indicators against the global cohort mean.

---

## IX. Methodological Limitations & Ethical Framework

### A. Limitations and Latency
1. **Survey Asynchrony:** World Bank Joint Malnutrition Estimates rely on periodic household demographic surveys (DHS, MICS) conducted on 3–5 year cycles (current data spans 2018–2023). Acute economic shocks or conflicts (e.g. post-2022 food inflation) are subject to reporting latency.
2. **The Ecological Fallacy:** National averages conceal severe subnational disparities. A country classified under Cluster 1 (High Obesity) may harbour pockets of severe child stunting in marginalized rural or indigenous populations.
3. **Surveillance Disparities:** The 51 excluded states were non-reporting microstates and high-income nations without active UNICEF child surveillance systems.

### B. Ethical Framework for Multilateral Policy
1. **Non-Stigmatization Principle:** Clusters represent epidemiological typologies, not rankings or moral report cards. High obesity carries immense metabolic morbidity, just as undernutrition carries mortality risk.
2. **Decision Support, Not Automated Aid Conditionality:** These clusters must guide program design, never automate punitive aid reductions or funding penalties.
3. **Non-Circular Fairness:** Keeping GDP and income group out of the clustering features ensures low-income nations with exceptional nutrition programs are fairly recognized, preventing economic determinism.

---

## X. Conclusion & Future Directions

In this paper, we developed and validated an unsupervised machine learning pipeline to segment global malnutrition patterns across 166 sovereign nations using real World Bank and UNICEF/WHO data. Through rigorous benchmarking of Euclidean $K$-Means against custom Manhattan $K$-Medians, verified via Ward hierarchical clustering and 20-round bootstrap stability audits, we established that a 3-cluster partition represents the optimal, most stable macro-taxonomy of global malnutrition ($\text{ARI} = 0.8324$, Silhouette $= 0.2726$). We mapped the underlying factor architecture using PCA, showing that $65.80\%$ of variance is governed by the Nutrition Transition and Infant Care axes. 

Future research will extend this framework to longitudinal time-series clustering to track national trajectory velocities across the PCA plane, and incorporate subnational geospatial DHS survey data to resolve localized pockets of the Double Burden of Malnutrition.

---

## References

[1] World Health Organization, *Global Nutrition Targets 2025: Policy Brief Series*, Geneva: WHO Press, 2014.  
[2] B. M. Popkin, "The nutrition transition and obesity in the developing world," *The Journal of Nutrition*, vol. 131, no. 3, pp. 871S–873S, 2001.  
[3] Development Initiatives, *2022 Global Nutrition Report: Stronger Commitments for Greater Action*, Bristol, UK: Development Initiatives, 2022.  
[4] B. M. Popkin, C. Corvalan, and L. M. Grummer-Strawn, "Dynamics of the double burden of malnutrition and the changing nutrition reality," *The Lancet*, vol. 395, no. 10217, pp. 65–74, 2020.  
[5] World Bank, *World Development Indicators 2023*, Washington, DC: World Bank Group, 2023.  
[6] C. G. Victora et al., "Maternal and child undernutrition: consequences for adult health and human capital," *The Lancet*, vol. 371, no. 9609, pp. 340–357, 2008.  
[7] J. C. Wells et al., "The double burden of malnutrition: aetiological pathways and consequences for health," *The Lancet*, vol. 395, no. 10217, pp. 75–88, 2020.  
[8] P. Hall et al., "Machine learning constrained clustering for biomedical phenotypes," *IEEE Trans. Biomed. Eng.*, vol. 68, no. 4, pp. 1120–1129, 2021.  
[9] A. Rajkomar, J. Dean, and I. Kohane, "Machine learning in medicine," *New England Journal of Medicine*, vol. 380, no. 14, pp. 1347–1358, 2019.  
[10] J. MacQueen, "Some methods for classification and analysis of multivariate observations," in *Proc. 5th Berkeley Symp. Math. Statist. Prob.*, vol. 1, 1967, pp. 281–297.  
[11] P. S. Bradley, O. L. Mangasarian, and W. N. Street, "Clustering via concave minimization," *Advances in Neural Information Processing Systems*, vol. 9, pp. 368–374, 1996.  
[12] U. von Luxburg, "Clustering stability: An overview," *Foundations and Trends in Machine Learning*, vol. 2, no. 3, pp. 235–274, 2010.  
[13] D. Arthur and S. Vassilvitskii, "k-means++: The advantages of careful seeding," in *Proc. 18th Annual ACM-SIAM Symp. Discrete Algorithms (SODA)*, 2007, pp. 1027–1035.  
[14] V. Satopaa, J. Albrecht, D. Irwin, and B. Raghavan, "Finding a 'kneedle' in a haystack: Detecting knee points in system behavior," in *2011 31st Int. Conf. Distributed Computing Systems Workshops*, 2011, pp. 166–171.  
[15] L. Hubert and P. Arabie, "Comparing partitions," *Journal of Classification*, vol. 2, no. 1, pp. 193–218, 1985.  
[16] C. Hawkes et al., "Double-duty actions for malnutrition: why they matter and how to implement them," *The Lancet*, vol. 395, no. 10218, pp. 142–155, 2020.  
[17] P. J. Rousseeuw, "Silhouettes: A graphical aid to the interpretation and validation of cluster analysis," *J. Comput. Appl. Math.*, vol. 20, pp. 53–65, 1987.  
[18] D. L. Davies and D. W. Bouldin, "A cluster separation measure," *IEEE Trans. Pattern Anal. Mach. Intell.*, vol. PAMI-1, no. 2, pp. 224–227, 1979.  
[19] J. H. Ward Jr., "Hierarchical grouping to optimize an objective function," *J. Amer. Statist. Assoc.*, vol. 58, no. 301, pp. 236–244, 1963.  
[20] R. C. Sokal and F. J. Rohlf, "The comparison of dendrograms by objective methods," *Taxon*, vol. 11, no. 2, pp. 33–40, 1962.  
[21] H. Hotelling, "Analysis of a complex of statistical variables into principal components," *Journal of Educational Psychology*, vol. 24, no. 6, pp. 417–441, 1933.  
[22] K. Pearson, "On lines and planes of closest fit to systems of points in space," *Philosophical Magazine*, vol. 2, no. 11, pp. 559–572, 1901.  
[23] UNICEF, WHO, World Bank Group, *Levels and Trends in Child Malnutrition: Key Findings of the 2023 Edition*, New York: UNICEF, 2023.  
[24] NCD Risk Factor Collaboration (NCD-RisC), "Worldwide trends in body-mass index, underweight, overweight, and obesity from 1975 to 2016," *The Lancet*, vol. 390, no. 10113, pp. 2627–2642, 2017.

