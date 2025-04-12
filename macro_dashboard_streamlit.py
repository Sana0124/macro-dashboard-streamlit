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
    '20Y Treasury Bond ETF (TLT)': 'TLT'
    # Add more tickers as needed
}

# --- FETCH YFINANCE DATA ---
@st.cache_data
def get_stock_data(ticker):
    try:
        data = yf.download(ticker, start=start_date, end=today, auto_adjust=False)
        if 'Close' in data.columns and not data['Close'].empty:
            return data['Close']
        else:
            st.warning(f"No 'Close' price found for {ticker}.")
            return pd.Series(dtype=float)
    except Exception as e:
        st.warning(f"Failed to fetch data for {ticker}: {e}")
        return pd.Series(dtype=float)

# --- FETCH FRED DATA ---
@st.cache_data
def get_latest_fred_value(series):
    try:
        return fred.get_series(series).dropna().iloc[-1]
    except Exception as e:
        st.warning(f"Failed to fetch FRED data for {series}: {e}")
        return None

# --- MACRO DATA ---
cpi = get_latest_fred_value('CPIAUCSL') or 0
core_cpi = get_latest_fred_value('CPILFESL') or 0
ppi = get_latest_fred_value('PPIACO') or 0
m2 = get_latest_fred_value('M2SL') or 0
fed_funds = get_latest_fred_value('FEDFUNDS') or 0
reverse_repo = get_latest_fred_value('RRPONTSYD') or 0

# --- MARKET DATA ---
spx = get_stock_data('^GSPC')
tlt = get_stock_data('TLT')
dxy = get_stock_data('DX-Y.NYB')
vix = get_stock_data('^VIX')

# --- TREND FUNCTION ---
def trend(data):
    if data.empty or len(data) < 2:
        return "No Data"
    if data.iloc[-1] > data.iloc[0]: return "📈 Up"
    elif data.iloc[-1] < data.iloc[0]: return "📉 Down"
    else: return "➖ Flat"

# --- TREND SUMMARY ---
st.subheader("🔍 Trend Summary (Past 6 Months)")
col1, col2, col3 = st.columns(3)
with col1:
    spx_val = f"{spx.iloc[-1]:,.0f}" if not spx.empty else "N/A"
    st.metric("📊 S&P 500", spx_val, trend(spx))
    tlt_val = f"${tlt.iloc[-1]:.2f}" if not tlt.empty else "N/A"
    st.metric("📉 TLT (Bonds)", tlt_val, trend(tlt))
with col2:
    dxy_val = f"{dxy.iloc[-1]:.2f}" if not dxy.empty else "N/A"
    st.metric("💵 DXY (USD Index)", dxy_val, trend(dxy))
    vix_val = f"{vix.iloc[-1]:.2f}" if not vix.empty else "N/A"
    st.metric("⚠️ VIX", vix_val, trend(vix))
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

if not tlt.empty and tlt.iloc[-1] > tlt.mean():
    st.info("📉 Bonds are gaining — investors seeking safety. Monitor yield compression.")

st.markdown("---")
st.caption("Built with real-time FRED + Yahoo Finance data")
