"""
etl_chicago.py
────────────────────────────────────────────────
Cleans the raw Chicago crime CSV and outputs a
standardized file ready to load into SQL.

Input:  data/raw/chicago_crime.csv
Output: data/clean/chicago_crime_clean.csv

Run:
    python etl_chicago.py
────────────────────────────────────────────────
"""

import pandas as pd
import os
from crime_categories import CRIME_CATEGORY_MAP

os.makedirs("data/clean", exist_ok=True)

INPUT  = "Data/raw/chicago_data.csv"
OUTPUT = "Data/clean/chicago_data_clean.csv"


def clean_chicago(input_path: str, output_path: str):
    print("Loading Chicago data...")
    df = pd.read_csv(input_path)
    print(f"  Raw rows: {len(df):,}")

    out = pd.DataFrame()

    # ── Date & Time ─────────────────────────────
    dates = pd.to_datetime(df["Date"], errors="coerce")

    out["case_id"]          = df["Case Number"].astype(str).str.strip()
    out["offense_datetime"] = dates.dt.strftime("%Y-%m-%d %H:%M:%S")
    out["year"]             = dates.dt.year
    out["month"]            = dates.dt.month
    out["day"]              = dates.dt.day
    out["hour"]             = dates.dt.hour
    out["day_of_week"]      = dates.dt.day_name()  

    # ── Crime Category ──────────────────────────
    raw                     = df["Primary Type"].str.upper().str.strip()
    out["crime_type_raw"]   = raw
    out["crime_category"]   = raw.map(CRIME_CATEGORY_MAP).fillna("Other")

    # ── Location ────────────────────────────────
    out["block_address"]    = df["Block"].astype(str).str.strip()
    out["latitude"]         = pd.to_numeric(df["Latitude"],  errors="coerce").round(6)
    out["longitude"]        = pd.to_numeric(df["Longitude"], errors="coerce").round(6)

    # ── Police Zone ─────────────────────────────
    out["beat"]             = df["Beat"].astype(str).str.strip()
    out["district"]         = df["District"].astype(str).str.strip()
    out["ward"]             = df["Ward"].astype(str).str.strip()
    out["community_area"]   = df["Community Area"].astype(str).str.strip()

    # ── Chicago-Specific ────────────────────────
    out["crime_description"]    = df["Description"].astype(str).str.strip()
    out["location_description"] = df["Location Description"].astype(str).str.strip()
    out["iucr_code"]            = df["IUCR"].astype(str).str.strip()
    out["fbi_code"]             = df["FBI Code"].astype(str).str.strip()

    # Store as 1/0 integers — universally supported in SQL
    out["arrest_made"]      = df["Arrest"].astype(str).str.lower().map({"true": 1, "false": 0})
    out["domestic"]         = df["Domestic"].astype(str).str.lower().map({"true": 1, "false": 0})

    # ── Drop rows missing critical fields ───────
    before = len(out)
    out = out.dropna(subset=["latitude", "longitude"])

    bad_dates = out["offense_datetime"].isna().sum()
    if bad_dates > 0:
        print(f"  Warning: {bad_dates:,} rows have an unparseable date — kept but offense_datetime will be null")

    dropped = before - len(out)
    print(f"  Dropped:   {dropped:,} rows (missing latitude or longitude)")
    print(f"  Clean rows:{len(out):,}")

    # ── Check for unmapped crime types ──────────
    unmapped = out.loc[out["crime_category"] == "Other", "crime_type_raw"].unique()

    if len(unmapped) > 0:
        print(f"\n  Note: {len(unmapped)} unmapped crime type(s) labeled 'Other'.")
        print(f"  Add them to crime_categories.py if needed:")
        for u in unmapped:
            print(f"    \"{u}\"")

    out.to_csv(output_path, index=False)
    print(f"\n  Saved -> {output_path}")


if __name__ == "__main__":
    print("=" * 45)
    print("CHICAGO ETL")
    print("=" * 45)
    clean_chicago(INPUT, OUTPUT)
    print("\nDone! Load data/clean/chicago_crime_clean.csv")
    print("into SQL as a table named: chicago_crime")