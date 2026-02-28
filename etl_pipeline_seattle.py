"""
etl_seattle.py
────────────────────────────────────────────────
Cleans the raw Seattle crime CSV and outputs a
standardized file ready to load into SQL.

Input:  data/raw/seattle_crime.csv
Output: data/clean/seattle_crime_clean.csv

Run:
    python etl_seattle.py
────────────────────────────────────────────────
"""

import pandas as pd
import os
from crime_categories import CRIME_CATEGORY_MAP

os.makedirs("data/clean", exist_ok=True)

INPUT  = "Data/raw/seattle_data.csv"
OUTPUT = "Data/clean/seattle_data_clean.csv"


def clean_seattle(input_path: str, output_path: str):
    print("Loading Seattle data...")
    df = pd.read_csv(input_path)
    print(f"  Raw rows: {len(df):,}")

    out = pd.DataFrame()

    # ── Date & Time ─────────────────────────────
    dates = pd.to_datetime(df["Offense Date"], errors="coerce")

    out["case_id"]          = df["Report Number"].astype(str).str.strip()
    out["offense_datetime"] = dates.dt.strftime("%Y-%m-%d %H:%M:%S")
    out["year"]             = dates.dt.year
    out["month"]            = dates.dt.month
    out["day"]              = dates.dt.day
    out["hour"]             = dates.dt.hour
    out["day_of_week"]      = dates.dt.day_name()   # e.g. "Monday"

    # ── Crime Category ──────────────────────────
    raw                     = df["NIBRS Offense Code Description"].str.upper().str.strip()
    out["crime_type_raw"]   = raw
    out["crime_category"]   = raw.map(CRIME_CATEGORY_MAP).fillna("Other")

    # ── Location ────────────────────────────────
    out["block_address"]    = df["Block Address"].astype(str).str.strip()
    out["latitude"]         = pd.to_numeric(df["Latitude"],  errors="coerce").round(6)
    out["longitude"]        = pd.to_numeric(df["Longitude"], errors="coerce").round(6)

    # ── Police Zone ─────────────────────────────
    out["beat"]             = df["Beat"].astype(str).str.strip()
    out["precinct"]         = df["Precinct"].astype(str).str.strip()
    out["sector"]           = df["Sector"].astype(str).str.strip()

    # ── Seattle-Specific ────────────────────────
    out["neighborhood"]     = df["Neighborhood"].astype(str).str.strip()
    out["nibrs_group"]      = df["NIBRS Group AB"].astype(str).str.strip()
    out["nibrs_code"]       = df["NIBRS_offense_code"].astype(str).str.strip()
    out["shooting_type"]    = df["Shooting Type Group"].astype(str).str.strip()

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
    print("SEATTLE ETL")
    print("=" * 45)
    clean_seattle(INPUT, OUTPUT)
    print("\nDone! Load Data/clean/seattle_data_clean.csv")
    print("into SQL as a table named: seattle_crime")