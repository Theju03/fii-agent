# fii_scraper.py
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_top_fii_stocks():
    url = "https://trendlyne.com/fundamentals/fii-dii-activity/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]
        df.columns = df.columns.droplevel(0) if isinstance(df.columns, pd.MultiIndex) else df.columns
        df = df.rename(columns={
            'Company Name': 'Company',
            'FII Holdings (%)': 'FII Holdings (%)',
            'Change in FII (%)': 'Change (%)'
        })
        df = df[['Company', 'FII Holdings (%)', 'Change (%)']]
        df = df[df['Change (%)'] > 0].sort_values(by='Change (%)', ascending=False)
        return df.head(10)
    except Exception as e:
        print(f"Error fetching FII data: {e}")
        return pd.DataFrame(columns=['Company', 'FII Holdings (%)', 'Change (%)'])
