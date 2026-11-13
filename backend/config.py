"""
Configuration and Hyperparameters
Country Malnutrition Pattern Segmentation Using Health Indicators and Clustering
Course: Unsupervised Learning (Units II, III, IV)
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
FRONTEND_DATA_DIR = PROJECT_DIR / "frontend" / "data"

RAW_DATA_PATH = DATA_RAW_DIR / "nutrition_indicators.csv"
RESULTS_JSON_PATH = OUTPUTS_DIR / "results.json"
RESULTS_JS_PATH = FRONTEND_DATA_DIR / "results.js"
MODEL_COMPARISON_CSV_PATH = OUTPUTS_DIR / "model_comparison.csv"

# Reproducibility
RANDOM_SEED = 42

# World Bank API Configuration
WB_BASE_API = "https://api.worldbank.org/v2"
USER_AGENT = "MalnutritionClusteringProject/1.0 (University Research; Bill & Melinda Gates Foundation Context)"
REQUEST_TIMEOUT_SECONDS = 25
MAX_RETRIES = 4
RETRY_BACKOFF_FACTOR = 1.5

# Malnutrition Indicators to query
# Format: internal_key -> { "code": World Bank Indicator Code, "name": Display Name, "type": category }
INDICATORS = {
    "stunting": {
        "code": "SH.STA.STNT.ZS",
        "name": "Child Stunting (% children under 5)",
        "type": "undernutrition",
        "description": "Prevalence of stunting, height for age (% of children under 5 who are more than -2 SD below median)"
    },
    "wasting": {
        "code": "SH.STA.WAST.ZS",
        "name": "Child Wasting (% children under 5)",
        "type": "undernutrition",
        "description": "Prevalence of wasting, weight for height (% of children under 5 who are more than -2 SD below median)"
    },
    "underweight": {
        "code": "SH.STA.MALN.ZS",
        "name": "Child Underweight (% children under 5)",
        "type": "undernutrition",
        "description": "Prevalence of underweight, weight for age (% of children under 5)"
    },
    "undernourishment": {
        "code": "SN.ITK.DEFC.ZS",
        "name": "Prevalence of Undernourishment (% population)",
        "type": "undernutrition",
        "description": "Share of the population whose food consumption is insufficient to continuously provide dietary energy"
    },
    "anaemia_children": {
        "code": "SH.ANM.CHLD.ZS",
        "name": "Child Anaemia (% ages 6-59 months)",
        "type": "undernutrition",
        "description": "Prevalence of anaemia among children (% of children ages 6-59 months, Hb < 110 g/L)"
    },
    "anaemia_women": {
        "code": "SH.ANM.ALLW.ZS",
        "name": "Women Anaemia (% ages 15-49 years)",
        "type": "undernutrition",
        "description": "Prevalence of anaemia among women of reproductive age (% of women ages 15-49)"
    },
    "low_birthweight": {
        "code": "SH.STA.LBWT.ZS",
        "name": "Low Birthweight (% births)",
        "type": "undernutrition",
        "description": "Low-birthweight babies (% of births < 2,500g)"
    },
    "exclusive_breastfeeding": {
        "code": "SH.STA.BFED.ZS",
        "name": "Exclusive Breastfeeding (% under 6 months)",
        "type": "protective_nutrition",
        "description": "Exclusive breastfeeding (% of children under 6 months)"
    },
    "child_overweight": {
        "code": "SH.STA.OWGH.ZS",
        "name": "Child Overweight (% children under 5)",
        "type": "overnutrition",
        "description": "Prevalence of overweight, weight for height (% of children under 5 who are more than +2 SD above median)"
    },
    "adult_obesity": {
        "code": "SH.STA.OB18.ZS",
        "name": "Adult Obesity (% population 18+)",
        "type": "overnutrition",
        "description": "Prevalence of obesity, total (% of adults ages 18+ with BMI >= 30)"
    },
    "adult_obesity_fe": {
        "code": "SH.STA.OB18.FE.ZS",
        "name": "Adult Female Obesity (%)",
        "type": "overnutrition",
        "description": "Prevalence of obesity, female (% of adults ages 18+ with BMI >= 30)"
    },
    "adult_obesity_ma": {
        "code": "SH.STA.OB18.MA.ZS",
        "name": "Adult Male Obesity (%)",
        "type": "overnutrition",
        "description": "Prevalence of obesity, male (% of adults ages 18+ with BMI >= 30)"
    },
    # Context variable only (NEVER used in clustering feature set to avoid circularity)
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.CD",
        "name": "GDP per capita (current US$)",
        "type": "context",
        "description": "GDP per capita in current US Dollars. Strictly contextual, excluded from feature vector."
    }
}

# Preprocessing Thresholds
INDICATOR_MISSING_THRESHOLD = 0.40   # Drop indicators missing for >40% of countries
COUNTRY_MISSING_THRESHOLD = 0.50     # Drop countries missing >50% of kept indicators
CORRELATION_DROP_THRESHOLD = 0.92    # Drop near-duplicate indicators (|r| > 0.92, keep first)
WINSORIZE_LOWER_QUANTILE = 0.01      # 1st percentile
WINSORIZE_UPPER_QUANTILE = 0.99      # 99th percentile

# Categorical Income Group Ordinal Encoding
INCOME_GROUP_MAPPING = {
    "Low income": 1,
    "Lower middle income": 2,
    "Upper middle income": 3,
    "High income": 4
}

# Clustering Hyperparameters
K_VALUES = [3, 4, 5, 6, 7, 8]
KMEANS_N_INIT = 20
KMEANS_MAX_ITER = 300
MIN_CLUSTER_SIZE_THRESHOLD = 5

# Bootstrap Stability Parameters
BOOTSTRAP_N_ROUNDS = 20
BOOTSTRAP_SUBSAMPLE_RATIO = 0.80

# Borderline country threshold (silhouette score)
BORDERLINE_SILHOUETTE_THRESHOLD = 0.05

