import pandas as pd
import requests
import os
import sys

def check_and_update():
    # Example URL of the raw data source
    DATA_URL = "https://example.com/api/v1/latest_metrics.csv"
    LOCAL_PATH = "data/workflow_metrics.csv"
    
    # 1. Fetch the remote data
    response = requests.get(DATA_URL)
    if response.status_code != 200:
        print("Failed to fetch data from source site.")
        sys.exit(0) # Exit peacefully
        
    remote_df = pd.read_csv(DATA_URL)
    
    # 2. Check if local data exists to compare
    if os.path.exists(LOCAL_PATH):
        local_df = pd.read_csv(LOCAL_PATH)
        
        # Compare row counts, last dates, or hashes to see if it's truly "new"
        if len(remote_df) == len(local_df):
            print("No new data detected on the site. Skipping update.")
            sys.exit(0) # Stop the workflow early without committing
            
    # 3. If data is new or local file doesn't exist, overwrite/append
    os.makedirs('data', exist_ok=True)
    remote_df.to_csv(LOCAL_PATH, index=False)
    print("New data found and updated locally!")

if __name__ == "__main__":
    check_and_update()