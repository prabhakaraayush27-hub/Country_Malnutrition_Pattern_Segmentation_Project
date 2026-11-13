"""
make_demo_data.py
Creates an offline DEMO synthetic dataset for fallback/offline unit testing.
STRICT REQUIREMENT: Synthetic data is strictly for offline fallback testing.
Whenever demo data is used, the system flags `is_demo = True` and displays
a prominent 'DEMO DATA' banner on the web dashboard.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from config import BASE_DIR, RANDOM_SEED, INDICATORS

def generate_demo_dataset(n_countries=180, output_path=None):
    if output_path is None:
        output_path = BASE_DIR / "data" / "raw" / "DEMO_nutrition_indicators.csv"
        
    np.random.seed(RANDOM_SEED)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    regions = [
        "Sub-Saharan Africa", "South Asia", "East Asia & Pacific",
        "Latin America & Caribbean", "Middle East & North Africa",
        "Europe & Central Asia", "North America"
    ]
    income_groups = ["Low income", "Lower middle income", "Upper middle income", "High income"]
    
    rows = []
    # 4 archetypes to ensure representative test patterns
    archetypes = ["undernutrition", "obesity", "double_burden", "better_conditions"]
    
    for i in range(n_countries):
        arch = archetypes[i % len(archetypes)]
        iso = f"DM{i+1:03d}"
        cname = f"Demo Country {i+1} ({arch})"
        
        if arch == "undernutrition":
            region = np.random.choice(["Sub-Saharan Africa", "South Asia"], p=[0.7, 0.3])
            income = np.random.choice(["Low income", "Lower middle income"], p=[0.7, 0.3])
            stunting = np.random.normal(36, 6)
            wasting = np.random.normal(9, 3)
            underweight = np.random.normal(24, 5)
            undernourishment = np.random.normal(22, 6)
            anaemia_chld = np.random.normal(58, 8)
            anaemia_wmn = np.random.normal(42, 7)
            bfed = np.random.normal(55, 12)
            owgh = np.random.normal(3.5, 1.5)
            ob18_fe = np.random.normal(7, 2.5)
            ob18_ma = np.random.normal(4, 1.5)
            gdp = np.random.exponential(1200) + 400
        elif arch == "obesity":
            region = np.random.choice(["North America", "Europe & Central Asia", "Latin America & Caribbean"], p=[0.2, 0.5, 0.3])
            income = np.random.choice(["High income", "Upper middle income"], p=[0.6, 0.4])
            stunting = np.random.normal(6, 2)
            wasting = np.random.normal(1.8, 0.8)
            underweight = np.random.normal(2.5, 1.0)
            undernourishment = np.random.normal(3.5, 1.2)
            anaemia_chld = np.random.normal(12, 3)
            anaemia_wmn = np.random.normal(15, 3)
            bfed = np.random.normal(28, 8)
            owgh = np.random.normal(8.5, 2.5)
            ob18_fe = np.random.normal(31, 5)
            ob18_ma = np.random.normal(27, 4)
            gdp = np.random.exponential(25000) + 12000
        elif arch == "double_burden":
            region = np.random.choice(["Latin America & Caribbean", "Middle East & North Africa", "East Asia & Pacific"], p=[0.4, 0.3, 0.3])
            income = np.random.choice(["Lower middle income", "Upper middle income"], p=[0.5, 0.5])
            stunting = np.random.normal(24, 4)
            wasting = np.random.normal(5, 1.5)
            underweight = np.random.normal(14, 3)
            undernourishment = np.random.normal(11, 3)
            anaemia_chld = np.random.normal(35, 6)
            anaemia_wmn = np.random.normal(32, 5)
            bfed = np.random.normal(42, 10)
            owgh = np.random.normal(9.8, 2.2)
            ob18_fe = np.random.normal(25, 4)
            ob18_ma = np.random.normal(19, 3.5)
            gdp = np.random.exponential(5000) + 2500
        else: # better_conditions
            region = np.random.choice(["Europe & Central Asia", "East Asia & Pacific"], p=[0.7, 0.3])
            income = np.random.choice(["High income", "Upper middle income"], p=[0.8, 0.2])
            stunting = np.random.normal(4, 1.5)
            wasting = np.random.normal(1.2, 0.5)
            underweight = np.random.normal(1.5, 0.6)
            undernourishment = np.random.normal(2.5, 0.8)
            anaemia_chld = np.random.normal(9, 2)
            anaemia_wmn = np.random.normal(11, 2)
            bfed = np.random.normal(45, 9)
            owgh = np.random.normal(4.2, 1.2)
            ob18_fe = np.random.normal(15, 3)
            ob18_ma = np.random.normal(14, 3)
            gdp = np.random.exponential(35000) + 20000
            
        row = {
            "country_code": iso,
            "country_name": cname,
            "region": region,
            "income_group": income,
            "stunting": max(0.5, round(stunting, 1)),
            "wasting": max(0.2, round(wasting, 1)),
            "underweight": max(0.3, round(underweight, 1)),
            "undernourishment": max(0.5, round(undernourishment, 1)),
            "anaemia_children": max(2.0, round(anaemia_chld, 1)),
            "anaemia_women": max(3.0, round(anaemia_wmn, 1)),
            "low_birthweight": None, # Kept null like real WB data
            "exclusive_breastfeeding": max(5.0, round(bfed, 1)),
            "child_overweight": max(0.5, round(owgh, 1)),
            "adult_obesity": round((ob18_fe + ob18_ma) / 2.0, 2),
            "adult_obesity_fe": round(ob18_fe, 2),
            "adult_obesity_ma": round(ob18_ma, 2),
            "gdp_per_capita": round(gdp, 0)
        }
        
        # Inject realistic sparsity (5-10% missing randomly)
        for col in ["exclusive_breastfeeding", "wasting", "child_overweight"]:
            if np.random.rand() < 0.08:
                row[col] = None
                
        rows.append(row)
        
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"[DEMO DATA CREATED] Saved synthetic demo dataset to {output_path} ({df.shape[0]} rows)")
    return df

if __name__ == "__main__":
    generate_demo_dataset()

