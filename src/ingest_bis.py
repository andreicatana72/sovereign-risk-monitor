import requests
import pandas as pd

def run():
    print("Fetching BIS credit data...")
    url = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_TC/2.0/?format=csv"
    df = pd.read_csv(url)
    df.to_parquet("data/bis_raw.parquet", index=False)
    print(f"Done. {len(df)} rows saved to data/bis_raw.parquet")

if __name__ == "__main__":
    run()