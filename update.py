import os
from pathlib import Path

import pandas as pd
import requests


def check_and_update():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    csv_path = data_dir / "live_posts.csv"
    api_url = "https://jsonplaceholder.typicode.com/posts"

    response = requests.get(api_url, timeout=10)
    response.raise_for_status()

    payload = response.json()
    df = pd.DataFrame(payload)
    df.to_csv(csv_path, index=False)

    print(f"Saved {len(df)} records to {csv_path}")


if __name__ == "__main__":
    check_and_update()