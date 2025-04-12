import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from fredapi import Fred
import plotly.graph_objs as go

# --- CONFIG ---
FRED_API_KEY = '4ffd360c061b3be7718aba08508f96dd'  # Replace this with your actual API key
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="Macro Market Dashboard", layout="wide")
st.title("📊 Live Macro Market Dashboard")

# --- DATE RANGE ---
today = datetime.date.today()
start_date = today - datetime.timedelta(days=365)

# --- TICKERS ---
tickers = {
    'S&P 500 (SPX)': '^GSPC',
    'US Dollar Index (DXY)': 'DX-Y.NYB',
    'VIX (Volatility Index)': '^VIX',
    '20Y Treasury Bond ETF (TLT)': 'TLT'
}

yield_tickers = {
    '10Y Yield': '^TNX',
    '2Y Yield': '^IRX',
    '30Y Yield': '^TYX'
}

# --- FETCH DATA ---
def get_stock_data(ticker):
    data = yf.download(ticker, start=start_date, end=today)
    return data['Adj Close']

# --- FRED ECONOMIC DATA ---
def get_fred_data(series_id):
    return fred.get_series(series_id).last('12M')

# --- LAYOUT ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Market Indices")
    for name, ticker in tickers.items():
        data = get_stock_data(ticker)
        st.line_chart(data, height=200, use_container_width=True)

with col2:
    st.subheader("💵 Treasury Yields")
    for name, ticker in yield_tickers.items():
        data = get_stock_data(ticker)
        st.line_chart(data, height=200, use_container_width=True)

# --- ECONOMIC METRICS ---
st.subheader("📊 Inflation & Fed Metrics")

cpi = fred.get_series('CPIAUCSL')[-1]
core_cpi = fred.get_series('CPILFESL')[-1]
ppi = fred.get_series('PPIACO')[-1]
m2 = fred.get_series('M2SL')[-1]

fed_funds = fred.get_series('FEDFUNDS')[-1]
reverse_repo = fred.get_series('RRPONTSYD')[-1]

st.markdown(f"**🟢 CPI:** {cpi:.2f} | **Core CPI:** {core_cpi:.2f} | **PPI:** {ppi:.2f}")
st.markdown(f"**🔵 M2 Supply:** {m2/1e12:.2f} Trillion | **Fed Funds Rate:** {fed_funds:.2f}% | **Reverse Repo:** {reverse_repo:.2f}%")

# --- LOGIC BOXES ---
st.markdown("---")
st.subheader("🧠 Smart Logic Analysis")

if cpi < 3 and ppi < 3 and fed_funds > reverse_repo:
    st.success("✅ Inflation is easing. Fed may consider a pause or cut later in 2025.")
elif cpi > 3.5 and ppi > 3.5:
    st.warning("⚠️ Stagflation risk rising. Watch bond yields and SPX reaction.")
else:
    st.info("ℹ️ Inflation mixed. Wait for next CPI/PPI + Fed signals.")

# --- AUTO REFRESH ---
st_autorefresh = st.experimental_rerun
