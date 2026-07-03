import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Live Data Dashboard", layout="wide")
st.title("📡 Live Data Dashboard")

LOCAL_DATA_PATH = Path("data/popular_shows_dataset.csv")


def load_local_data() -> pd.DataFrame:
    if not LOCAL_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found: {LOCAL_DATA_PATH}")
    return pd.read_csv(LOCAL_DATA_PATH)


if st.sidebar.button("Reload local file"):
    st.cache_data.clear()

@st.cache_data
def get_data() -> pd.DataFrame:
    return load_local_data()

try:
    df = get_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

st.caption(f"Using local file: {LOCAL_DATA_PATH}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Year Range", f"{int(df['year'].min())} - {int(df['year'].max())}")
col3.metric("Highest Revenue", f"${int(df['revenue'].max()):,}")

st.subheader("Latest Records")
st.dataframe(df.head(20), width="stretch")

st.subheader("Revenue by Year")
revenue_by_year = df.groupby("year")["revenue"].sum().reset_index()
st.bar_chart(revenue_by_year.set_index("year"))