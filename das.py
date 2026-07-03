import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Live Data Dashboard", layout="wide")
st.title("📡 Live Data Dashboard")

DATA_URL = "https://jsonplaceholder.typicode.com/posts"
LOCAL_DATA_PATH = Path("data/live_posts.csv")


def fetch_and_store_data(force_refresh: bool = False) -> pd.DataFrame:
    LOCAL_DATA_PATH.parent.mkdir(exist_ok=True)

    if force_refresh or not LOCAL_DATA_PATH.exists():
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()
        df = pd.DataFrame(payload)
        df.to_csv(LOCAL_DATA_PATH, index=False)
        st.session_state["last_updated"] = pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        return df

    return pd.read_csv(LOCAL_DATA_PATH)


if "last_updated" not in st.session_state:
    st.session_state["last_updated"] = "Not fetched yet"

if st.sidebar.button("Refresh data"):
    try:
        df = fetch_and_store_data(force_refresh=True)
        st.sidebar.success("Data refreshed and saved locally.")
    except requests.RequestException as exc:
        st.sidebar.warning(f"Could not fetch remote data: {exc}")
        df = pd.read_csv(LOCAL_DATA_PATH) if LOCAL_DATA_PATH.exists() else pd.DataFrame()
else:
    try:
        df = fetch_and_store_data(force_refresh=False)
    except requests.RequestException as exc:
        st.sidebar.warning(f"Using the last saved local copy. Remote fetch failed: {exc}")
        df = pd.read_csv(LOCAL_DATA_PATH) if LOCAL_DATA_PATH.exists() else pd.DataFrame()

if df.empty:
    st.info("No data available yet. Click Refresh data to fetch from the public API.")
    st.stop()

st.caption(f"Stored locally at {LOCAL_DATA_PATH}")
st.caption(f"Last refresh: {st.session_state['last_updated']}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Users Covered", df["userId"].nunique())
col3.metric("Latest Post ID", int(df["id"].max()))

st.subheader("Latest Records")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Post Count by User")
user_counts = df.groupby("userId").size().reset_index(name="post_count")
st.bar_chart(user_counts.set_index("userId"))