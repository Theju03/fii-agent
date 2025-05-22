import requests
import pandas as pd
from datetime import datetime

def get_nse_session():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.nseindia.com/market-data/equity-derivatives-bulk-block-deals',
        'Origin': 'https://www.nseindia.com',
    }
    session = requests.Session()
    session.get('https://www.nseindia.com', headers=headers)
    return session, headers

def fetch_live_bulk_deals(date_str):
    session, headers = get_nse_session()
    url = f'https://www.nseindia.com/api/equity-bulk-deals?date={date_str}'
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        data_json = response.json()
        df = pd.DataFrame(data_json['data'])
        return df
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return pd.DataFrame()

def filter_fii_transactions(df):
    fii_keywords = ['FII', 'Foreign Institutional Investor', 'Foreign Portfolio Investor']
    mask = df['clientName'].str.contains('|'.join(fii_keywords), case=False, na=False)
    return df[mask]

def aggregate_fii_activity(df):
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    df['buySell'] = df['buySell'].str.upper()
    df['netQty'] = df.apply(lambda x: x['quantity'] if x['buySell']=='BUY' else -x['quantity'], axis=1)
    agg = df.groupby('securityName')['netQty'].sum().reset_index()
    agg = agg.sort_values(by='netQty', ascending=False)
    return agg

def get_fii_portfolio():
    date_str = datetime.today().strftime('%d-%m-%Y')
    df_bulk = fetch_live_bulk_deals(date_str)
    if df_bulk.empty:
        print("No bulk deal data available today.")
        return pd.DataFrame()
    df_fii = filter_fii_transactions(df_bulk)
    if df_fii.empty:
        print("No FII transactions today.")
        return pd.DataFrame()
    agg_fii = aggregate_fii_activity(df_fii)
    return agg_fii

if __name__ == "__main__":
    portfolio_df = get_fii_portfolio()
    print(portfolio_df.head(10))
