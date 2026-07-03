from pathlib import Path

import pandas as pd


# If you want to fetch from a URL later, you can keep that logic here as comments.
# Example:
# DATA_URL = "https://example.com/data.csv"
# LOCAL_PATH = Path("data/popular_shows_dataset.csv")
#
# def fetch_from_url(url: str) -> pd.DataFrame: #  IF WE REFRESH INTENERT URL AND STORE TO FILE THE VISUALIZE HAPPEN
#     import requests
#     response = requests.get(url, timeout=30)
#     response.raise_for_status()
#     return pd.read_csv(response.url)

LOCAL_PATH = Path("data/popular_shows_dataset.csv")


def check_and_update(local_path: Path = LOCAL_PATH) -> None:
    local_path.parent.mkdir(exist_ok=True)

    if not local_path.exists():
        raise FileNotFoundError(f"Local dataset not found: {local_path}")

    df = pd.read_csv(local_path)

    if df.empty:
        raise ValueError("The local dataset is empty.")

    print(f"Loaded {len(df)} rows from {local_path}")


if __name__ == "__main__":
    check_and_update()