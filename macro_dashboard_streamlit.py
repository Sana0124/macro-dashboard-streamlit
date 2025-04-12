import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
from fredapi import Fred

# --- CONFIG ---
FRED_API_KEY = "4ffd360c061b3be7718aba08508f96dd"
fred = Fred(api_key=FRED_API_KEY)

st.set_page_config(page_title="Macro Intelligence Dashboard", layout="wide")
st.title("🧠 Macro Intelligence Dashboard")

# --- DATE RANGE ---
today = datetime.date.today()
start_date = today - datetime.timedelta(days=180)

# --- TICKERS ---
tickers = {
    'S&P 500 (SPX)': '^GSPC',
    'US Dollar Index (DXY)': 'DX-Y.NYB',
    'VIX (Volatility Index)': '^VIX',
    '20Y Treasury Bond ETF (TLT)': 'TLT',
    '10Y Yield': '^TNX',
    '2Y Yield': '^IRX',
    '30Y Yield': '^TYX'
}

# --- FETCH YFINANCE DATA ---
def get_stock_data(ticker):
    data = yf.download(ticker, start=start_date, end=today)
    return data['Close'] if 'Close' in data.columns else data.iloc[:, -1]

# --- FETCH FRED DATA ---
def get_latest_fred_value(series):
    return fred.get_series(series).dropna()[-1]

# --- MACRO DATA ---
cpi = get_latest_fred_value('CPIAUCSL')
core_cpi = get_latest_fred_value('CPILFESL')
ppi = get_latest_fred_value('PPIACO')
m2 = get_latest_fred_value('M2SL')
fed_funds = get_latest_fred_value('FEDFUNDS')
reverse_repo = get_latest_fred_value('RRPONTSYD')

# --- MARKET DATA ---
spx = get_stock_data('^GSPC')
tlt = get_stock_data('TLT')
dxy = get_stock_data('DX-Y.NYB')
vix = get_stock_data('^VIX')

def trend(data):
    if data.iloc[-1] > data.iloc[0]: return "📈 Up"
    elif data.iloc[-1] < data.iloc[0]: return "📉 Down"
    else: return "➖ Flat"

st.subheader("🔍 Trend Summary (Past 6 Months)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 S&P 500", f"{spx.iloc[-1]:,.0f}", trend(spx))
    st.metric("📉 TLT (Bonds)", f"${tlt.iloc[-1]:.2f}", trend(tlt))
with col2:
    st.metric("💵 DXY (USD Index)", f"{dxy.iloc[-1]:.2f}", trend(dxy))
    st.metric("⚠️ VIX", f"{vix.iloc[-1]:.2f}", trend(vix))
with col3:
    st.metric("📊 CPI", f"{cpi:.2f}")
    st.metric("🏦 M2 Supply (T)", f"{m2/1e12:.2f} T")

# --- MACRO LOGIC ---
st.subheader("🧠 Market Intelligence Summary")

if cpi < 3 and ppi < 3:
    st.success("🟢 Inflation is easing — risk assets may outperform. Watch equities.")
elif cpi > 3.5 and ppi > 3.5:
    st.warning("🟠 Stagflation signals — inflation and producer costs both high.")
else:
    st.info("🟡 Mixed inflation — wait for next macro releases to confirm trend.")

if fed_funds > 4 and reverse_repo > 50:
    st.warning("🔵 Fed is still restrictive — liquidity tight. No immediate pivot expected.")
else:
    st.success("🟢 Liquidity improving — Fed may soften tone if inflation continues easing.")

if tlt.iloc[-1] > tlt.mean():
    st.info("📉 Bonds are gaining — investors seeking safety. Monitor yield compression.")

st.markdown("---")
st.caption("Built with real-time FRED + Yahoo Finance data")
