{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 Menlo-Regular;\f2\fnil\fcharset0 AppleColorEmoji;
}
{\colortbl;\red255\green255\blue255;\red202\green23\blue113;\red199\green226\blue213;}
{\*\expandedcolortbl;;\cssrgb\c83922\c20000\c51765;\cssrgb\c81961\c90588\c86667;}
\margl1440\margr1440\vieww30040\viewh18900\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import pandas as pd\
import datetime\
from fredapi import Fred\
import plotly.graph_objs as go\
\
# --- CONFIG ---\
FRED_API_KEY = '
\f1\fs27\fsmilli13552 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 4ffd360c061b3be7718aba08508f96dd\'92
\f0\fs24 \cf0 \cb1 \kerning1\expnd0\expndtw0 \outl0\strokewidth0  \
fred = Fred(api_key=FRED_API_KEY)\
\
st.set_page_config(page_title="Macro Market Dashboard", layout="wide")\
st.title("
\f2 \uc0\u55357 \u56522 
\f0  Live Macro Market Dashboard")\
\
# --- DATE RANGE ---\
today = datetime.date.today()\
start_date = today - datetime.timedelta(days=365)\
\
# --- TICKERS ---\
tickers = \{\
    'S&P 500 (SPX)': '^GSPC',\
    'US Dollar Index (DXY)': 'DX-Y.NYB',\
    'VIX (Volatility Index)': '^VIX',\
    '20Y Treasury Bond ETF (TLT)': 'TLT'\
\}\
\
yield_tickers = \{\
    '10Y Yield': '^TNX',\
    '2Y Yield': '^IRX',\
    '30Y Yield': '^TYX'\
\}\
\
# --- FETCH DATA ---\
def get_stock_data(ticker):\
    data = yf.download(ticker, start=start_date, end=today)\
    return data['Adj Close']\
\
# --- FRED ECONOMIC DATA ---\
def get_fred_data(series_id):\
    return fred.get_series(series_id).last('12M')\
\
# --- LAYOUT ---\
col1, col2 = st.columns(2)\
with col1:\
    st.subheader("
\f2 \uc0\u55357 \u56520 
\f0  Market Indices")\
    for name, ticker in tickers.items():\
        data = get_stock_data(ticker)\
        st.line_chart(data, height=200, use_container_width=True)\
\
with col2:\
    st.subheader("
\f2 \uc0\u55357 \u56501 
\f0  Treasury Yields")\
    for name, ticker in yield_tickers.items():\
        data = get_stock_data(ticker)\
        st.line_chart(data, height=200, use_container_width=True)\
\
# --- ECONOMIC METRICS ---\
st.subheader("
\f2 \uc0\u55357 \u56522 
\f0  Inflation & Fed Metrics")\
\
cpi = fred.get_series('CPIAUCSL')[-1]\
core_cpi = fred.get_series('CPILFESL')[-1]\
ppi = fred.get_series('PPIACO')[-1]\
m2 = fred.get_series('M2SL')[-1]\
\
fed_funds = fred.get_series('FEDFUNDS')[-1]\
reverse_repo = fred.get_series('RRPONTSYD')[-1]\
\
st.markdown(f"**
\f2 \uc0\u55357 \u57314 
\f0  CPI:** \{cpi:.2f\} | **Core CPI:** \{core_cpi:.2f\} | **PPI:** \{ppi:.2f\}")\
st.markdown(f"**
\f2 \uc0\u55357 \u56629 
\f0  M2 Supply:** \{m2/1e12:.2f\} Trillion | **Fed Funds Rate:** \{fed_funds:.2f\}% | **Reverse Repo:** \{reverse_repo:.2f\}%")\
\
# --- LOGIC BOXES ---\
st.markdown("---")\
st.subheader("
\f2 \uc0\u55358 \u56800 
\f0  Smart Logic Analysis")\
\
if cpi < 3 and ppi < 3 and fed_funds > reverse_repo:\
    st.success("
\f2 \uc0\u9989 
\f0  Inflation is easing. Fed may consider a pause or cut later in 2025.")\
elif cpi > 3.5 and ppi > 3.5:\
    st.warning("
\f2 \uc0\u9888 \u65039 
\f0  Stagflation risk rising. Watch bond yields and SPX reaction.")\
else:\
    st.info("
\f2 \uc0\u8505 \u65039 
\f0  Inflation mixed. Wait for next CPI/PPI + Fed signals.")\
\
# --- AUTO REFRESH ---\
st_autorefresh = st.experimental_rerun\
}