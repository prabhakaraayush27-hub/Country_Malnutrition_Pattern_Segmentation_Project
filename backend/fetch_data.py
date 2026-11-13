"""
fetch_data.py
Automated ingestion of real nutrition indicators from the World Bank Open Data API.
Republishes UNICEF/WHO/World Bank Joint Child Malnutrition Estimates and WHO/NCD-RisC data.
"""

import sys
import io
import time
import zipfile
import argparse
import requests
import urllib3
import pandas as pd
from pathlib import Path

# Disable SSL insecure warnings if cert verify issues occur on local proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from config import (
    INDICATORS,
    RAW_DATA_PATH,
    USER_AGENT,
    REQUEST_TIMEOUT_SECONDS,
    MAX_RETRIES,
    RETRY_BACKOFF_FACTOR
)

def get_session():
    """Create a configured requests session with headers."""
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session

def fetch_country_list(session):
    """
    Fetch the list of countries from the World Bank API, excluding regional aggregates.
    Returns a DataFrame with columns: ['country_code', 'country_name', 'region', 'income_group'].
    """
    url = "https://api.worldbank.org/v2/country?format=json&per_page=400"
    print(f"[INFO] Fetching country master list from {url}...")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, verify=True)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) > 1 and isinstance(data[1], list):
                    countries = []
                    for c in data[1]:
                        region_info = c.get("region", {})
                        region_val = region_info.get("value", "").strip() if isinstance(region_info, dict) else ""
                        
                        # Filter out aggregates
                        if not region_val or region_val.lower() == "aggregates":
                            continue
                            
                        income_info = c.get("incomeLevel", {})
                        income_val = income_info.get("value", "").strip() if isinstance(income_info, dict) else ""
                        if income_val.lower() == "aggregates":
                            income_val = ""
                            
                        countries.append({
                            "country_code": c.get("id", "").strip(),
                            "country_name": c.get("name", "").strip(),
                            "region": region_val,
                            "income_group": income_val
                        })
                    
                    df_countries = pd.DataFrame(countries)
                    print(f"[SUCCESS] Retrieved {len(df_countries)} real sovereign countries (aggregates removed).")
                    return df_countries
        except Exception as e:
            print(f"[WARN] Country fetch attempt {attempt} failed: {e}")
            time.sleep(RETRY_BACKOFF_FACTOR * attempt)
            
    print("[ERROR] Failed to fetch country list from World Bank JSON API.")
    return None

def fetch_indicator_json(session, indicator_code):
    """
    Attempt to fetch the latest non-empty value for an indicator via the JSON API with mrnev=1.
    Returns dict: { country_iso3: (value, year) } or None if failed/timed out.
    """
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=1000&mrnev=1"
    try:
        resp = session.get(url, timeout=12, verify=True)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 1 and isinstance(data[1], list):
                results = {}
                for item in data[1]:
                    iso3 = item.get("countryiso3code")
                    val = item.get("value")
                    yr = item.get("date")
                    if iso3 and val is not None:
                        results[iso3.strip()] = (float(val), yr)
                if results:
                    return results
    except Exception:
        pass
    return None

def fetch_indicator_bulk_zip(session, indicator_code):
    """
    Download the bulk CSV zip archive for an indicator, extracting the latest non-null value per country.
    Returns dict: { country_iso3: (value, year) } or None if failed.
    """
    url = f"https://api.worldbank.org/v2/en/indicator/{indicator_code}?downloadformat=csv"
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS, verify=False)
            if resp.status_code == 200 and resp.content[:2] == b"PK":
                with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                    api_files = [f for f in z.namelist() if f.startswith("API_")]
                    if not api_files:
                        continue
                    with z.open(api_files[0]) as f:
                        df = pd.read_csv(f, skiprows=4)
                        year_cols = [c for c in df.columns if c.isdigit()]
                        if not year_cols:
                            continue
                        year_cols = sorted(year_cols, key=int)
                        
                        results = {}
                        for _, row in df.iterrows():
                            code = str(row.get("Country Code", "")).strip()
                            if not code:
                                continue
                            # Find the latest available year with non-null value
                            for yr in reversed(year_cols):
                                val = row.get(yr)
                                if pd.notna(val) and str(val).strip() != "":
                                    try:
                                        fval = float(val)
                                        results[code] = (fval, yr)
                                        break
                                    except ValueError:
                                        continue
                        if results:
                            return results
            elif resp.status_code == 502:
                # Gateway error, back off and retry
                time.sleep(RETRY_BACKOFF_FACTOR * attempt * 1.5)
        except Exception as e:
            time.sleep(RETRY_BACKOFF_FACTOR * attempt)
            
    return None

def fetch_indicator_data(session, indicator_key, indicator_meta):
    """
    Fetch data for an indicator using JSON endpoint first, falling back to bulk zip download.
    """
    code = indicator_meta["code"]
    name = indicator_meta["name"]
    
    print(f"[FETCH] Querying {name} (Code: {code})...", end=" ", flush=True)
    
    # 1. Try JSON API first
    results = fetch_indicator_json(session, code)
    if results:
        print(f"DONE (JSON API: {len(results)} countries with data)")
        return results
        
    # 2. Fallback to Bulk CSV Zip
    results = fetch_indicator_bulk_zip(session, code)
    if results:
        print(f"DONE (Bulk ZIP Fallback: {len(results)} countries with data)")
        return results
        
    print("FAILED (No data returned from either JSON or Bulk CSV endpoint)")
    return {}

def main():
    parser = argparse.ArgumentParser(description="Download World Bank Malnutrition Indicators")
    parser.add_argument("--data", type=str, default=None, help="Path to existing manual CSV file to use instead of fetching")
    parser.add_argument("--out", type=str, default=str(RAW_DATA_PATH), help="Output raw CSV path")
    args = parser.parse_args()

    # If manual data is provided, copy/load and validate
    if args.data:
        data_path = Path(args.data)
        if not data_path.exists():
            print(f"[ERROR] Specified data file {data_path} does not exist.")
            sys.exit(1)
        print(f"[INFO] Using provided dataset from {data_path}")
        df = pd.read_csv(data_path)
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
        print(f"[SUCCESS] Saved data to {out_path} ({df.shape[0]} rows, {df.shape[1]} columns)")
        return

    session = get_session()
    
    # Step 1: Country Master List
    df_countries = fetch_country_list(session)
    if df_countries is None or df_countries.empty:
        print("[CRITICAL] Could not obtain country master list. Aborting.")
        sys.exit(1)
        
    total_countries = len(df_countries)
    country_codes = set(df_countries["country_code"].tolist())
    
    # Step 2: Fetch Each Indicator
    indicator_data = {}
    coverage_report = []
    
    for key, meta in INDICATORS.items():
        data_dict = fetch_indicator_data(session, key, meta)
        indicator_data[key] = data_dict
        
        # Calculate coverage over valid countries
        valid_in_master = sum(1 for c in data_dict.keys() if c in country_codes)
        coverage_pct = (valid_in_master / total_countries) * 100 if total_countries > 0 else 0
        is_low = coverage_pct < 30.0
        
        coverage_report.append({
            "key": key,
            "name": meta["name"],
            "code": meta["code"],
            "category": meta["type"],
            "count": valid_in_master,
            "coverage_pct": round(coverage_pct, 1),
            "status": "LOW COVERAGE" if is_low else "USABLE"
        })
        time.sleep(1.0) # Graceful delay to respect API rate limits
        
    # Check for adult obesity synthesis if total obesity code was empty
    obesity_total_count = sum(1 for c in indicator_data.get("adult_obesity", {}).keys() if c in country_codes)
    obesity_fe_count = sum(1 for c in indicator_data.get("adult_obesity_fe", {}).keys() if c in country_codes)
    obesity_ma_count = sum(1 for c in indicator_data.get("adult_obesity_ma", {}).keys() if c in country_codes)
    
    if obesity_total_count == 0 and obesity_fe_count > 0 and obesity_ma_count > 0:
        print("[INFO] Synthesizing total adult obesity from female and male series (SH.STA.OB18.FE.ZS & SH.STA.OB18.MA.ZS)...")
        synth_obesity = {}
        fe_dict = indicator_data["adult_obesity_fe"]
        ma_dict = indicator_data["adult_obesity_ma"]
        for c in country_codes:
            if c in fe_dict and c in ma_dict:
                avg_val = (fe_dict[c][0] + ma_dict[c][0]) / 2.0
                synth_obesity[c] = (round(avg_val, 2), max(fe_dict[c][1], ma_dict[c][1]))
            elif c in fe_dict:
                synth_obesity[c] = fe_dict[c]
            elif c in ma_dict:
                synth_obesity[c] = ma_dict[c]
        indicator_data["adult_obesity"] = synth_obesity
        valid_synth = sum(1 for c in synth_obesity.keys() if c in country_codes)
        for r in coverage_report:
            if r["key"] == "adult_obesity":
                r["count"] = valid_synth
                r["coverage_pct"] = round((valid_synth / total_countries) * 100, 1)
                r["status"] = "USABLE (Averaged Female+Male)"
                
    # Step 3: Print Coverage Table
    print("\n" + "=" * 80)
    print("WORLD BANK INDICATOR COVERAGE AUDIT")
    print("=" * 80)
    print(f"{'Indicator Name':<38} {'Code':<18} {'Countries':<10} {'Coverage':<10} {'Status'}")
    print("-" * 80)
    usable_indicators_count = 0
    for r in coverage_report:
        print(f"{r['name'][:36]:<38} {r['code']:<18} {r['count']:<10} {r['coverage_pct']:<5}%     {r['status']}")
        if r["coverage_pct"] >= 30.0 and r["category"] != "context":
            usable_indicators_count += 1
    print("=" * 80)
    print(f"Total usable clustering indicators with >= 30% coverage: {usable_indicators_count}")
    
    # Requirement: abort without saving if fewer than 5 indicators have usable coverage
    if usable_indicators_count < 5:
        print(f"[CRITICAL ERROR] Only {usable_indicators_count} indicators have usable coverage (required >= 5). Aborting without saving.")
        sys.exit(1)
        
    # Step 4: Build Merged Dataset
    rows = []
    for _, country in df_countries.iterrows():
        c_code = country["country_code"]
        row = {
            "country_code": c_code,
            "country_name": country["country_name"],
            "region": country["region"],
            "income_group": country["income_group"]
        }
        for key in INDICATORS.keys():
            data_dict = indicator_data.get(key, {})
            val_tuple = data_dict.get(c_code)
            row[key] = val_tuple[0] if val_tuple is not None else None
        rows.append(row)
        
    df_merged = pd.DataFrame(rows)
    
    # Save raw CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(out_path, index=False)
    print(f"\n[SUCCESS] Saved merged real dataset to {out_path}")
    print(f"[DATASET SHAPE] {df_merged.shape[0]} countries x {df_merged.shape[1]} columns")

if __name__ == "__main__":
    main()

