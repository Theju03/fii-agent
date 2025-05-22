# app.py
import streamlit as st
import pandas as pd
from fii_scraper import fetch_top_fii_stocks

st.set_page_config(page_title="FII-Inspired Portfolio", layout="wide")
st.title("📈 FII-Inspired Investment Dashboard")

st.markdown("This dashboard shows Indian stocks where FIIs have recently increased their stake.")

with st.spinner("Fetching FII data..."):
    df = fetch_top_fii_stocks()

if df.empty:
    st.warning("Could not load data. Please try again later.")
else:
    st.dataframe(df, use_container_width=True)
    st.subheader("📊 Recommended Portfolio (Top 10)")
    st.write("Equally weighted portfolio of top 10 FII-favored companies:")
    df['Weight (%)'] = round(100 / len(df), 2)
    st.dataframe(df[['Company', 'FII Holdings (%)', 'Change (%)', 'Weight (%)']], use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "fii_portfolio.csv", "text/csv")
