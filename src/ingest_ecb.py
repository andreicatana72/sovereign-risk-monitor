import requests
import pandas as pd
from io import StringIO

SERIES = {
    "FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA": "euribor_3m",
    "FM/M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA": "euribor_6m",
    "FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA": "euribor_1y",
}

def fetch_ecb_series(series_key, series_name):
    url = (
        f"https://data-api.ecb.europa.eu/service/data/{series_key}"
        f"?format=csvdata"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"  Warning: Could not fetch {series_name} — status {response.status_code}")
        return pd.DataFrame()

    df = pd.read_csv(StringIO(response.text))
    df = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
    df.columns = ["date", series_name]
    df["date"] = pd.to_datetime(df["date"])
    df[series_name] = pd.to_numeric(df[series_name], errors="coerce")
    return df

def run():
    print("Fetching ECB data...")
    dfs = []
    for key, name in SERIES.items():
        print(f"  Fetching {name}...")
        df = fetch_ecb_series(key, name)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        print("No ECB data fetched.")
        return

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="date", how="outer")

    merged = merged.sort_values("date")
    merged.to_parquet("data/ecb_raw.parquet", index=False)
    print(f"Done. {len(merged)} rows saved to data/ecb_raw.parquet")

if __name__ == "__main__":
    run()