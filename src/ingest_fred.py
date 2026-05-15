import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import os

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

SERIES = {
    "VIXCLS":  "vix",
    "DGS10":   "us_10y_yield",
    "DGS2":    "us_2y_yield",
    "FEDFUNDS": "fed_funds_rate",
    "T10YIE":  "us_10y_breakeven_inflation",
}

def run():
    print("Fetching FRED data...")
    fred = Fred(api_key=FRED_API_KEY)
    dfs = []

    for series_id, name in SERIES.items():
        print(f"  Fetching {name}...")
        data = fred.get_series(series_id)
        df = data.reset_index()
        df.columns = ["date", name]
        dfs.append(df)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="date", how="outer")

    merged = merged.sort_values("date")
    merged.to_parquet("data/fred_raw.parquet", index=False)
    print(f"Done. {len(merged)} rows saved to data/fred_raw.parquet")

if __name__ == "__main__":
    run()