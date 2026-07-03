import os
from datetime import date, timedelta

import pandas as pd


def check_and_update():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "workflow_metrics.csv")
    excel_path = os.path.join(data_dir, "workflow_metrics.xlsx")

    start_date = date.today() - timedelta(days=29)
    rows = []

    for offset in range(30):
        current_date = start_date + timedelta(days=offset)
        rows.append(
            {
                "Date": current_date.strftime("%Y-%m-%d"),
                "Total_Tasks": 120 + (offset % 7) * 8,
                "Failed_Tasks": (offset + 2) % 6,
                "Avg_Duration_Min": 18 + ((offset * 3) % 9),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False, engine="openpyxl")

    print(f"Generated {len(df)} workflow records at {csv_path} and {excel_path}")


if __name__ == "__main__":
    check_and_update()