import requests
import pandas as pd

COUNTRIES = [
    # EU27
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI",
    "FR", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK",
    # Non-EU European
    "GB", "CH", "NO",
    # Global anchors
    "US", "JP"
]

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG":    "inflation",
    "GC.DOD.TOTL.GD.ZS": "debt_to_gdp",
    "BN.CAB.XOKA.GD.ZS": "current_account_gdp"
}

def fetch_indicator(indicator_code, indicator_name):
    country_str = ";".join(COUNTRIES)
    url = (
        f"https://api.worldbank.org/v2/country/{country_str}"
        f"/indicator/{indicator_code}"
        f"?format=json&per_page=1000&mrv=30"    # Get the most recent 30 years of data, which should cover 1990-2020
    )
    response = requests.get(url)
    data = response.json()
    records = []
    for entry in data[1]:
        records.append({
            "country": entry["countryiso3code"],
            "date": entry["date"],
            indicator_name: entry["value"]
        })
    return pd.DataFrame(records)

def run():
    print("Fetching World Bank data...")
    dfs = []
    for code, name in INDICATORS.items():
        print(f"  Fetching {name}...")
        df = fetch_indicator(code, name)
        dfs.append(df)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on=["country", "date"], how="outer")

    merged = merged.sort_values(["country", "date"])
    merged.to_parquet("data/worldbank_raw.parquet", index=False)
    print(f"Done. {len(merged)} rows saved to data/worldbank_raw.parquet")

if __name__ == "__main__":
    run()