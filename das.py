import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Operations Performance", layout="wide")
st.title("📊 Workflow Operations Performance Dashboard")

# Check if data exists
data_path = 'data/workflow_metrics.csv'
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # --- Metrics Rows ---
    latest = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Today's Total Tasks", int(latest['Total_Tasks']))
    col2.metric("Today's Failures", int(latest['Failed_Tasks']))
    col3.metric("Avg Duration", f"{latest['Avg_Duration_Min']} min")
    
    # --- Charts ---
    st.subheader("Performance Trends Over Time")
    st.line_chart(df.set_index('Date')[['Total_Tasks', 'Avg_Duration_Min']])
    
    # --- Raw Data View ---
    st.subheader("Raw Operations Data")
    st.dataframe(df)
else:
    st.warning("No data found. Wait for the automated pipeline or run the update script manually!")