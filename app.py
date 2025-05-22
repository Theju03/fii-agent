import streamlit as st
from fii_scraper import get_fii_portfolio  # Import the function you just made

def main():
    st.title("📈 Live FII-Inspired Investment Dashboard")

    portfolio_df = get_fii_portfolio()
    if portfolio_df.empty:
        st.info("No FII portfolio data available for today. Please try again later.")
    else:
        st.write("Top Stocks with FII Stake Increase Today:")
        st.dataframe(portfolio_df.head(10))

if __name__ == "__main__":
    main()
