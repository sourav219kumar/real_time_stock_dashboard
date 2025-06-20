
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Streamlit config
st.set_page_config(page_title="📈 Real-Time Stock Dashboard", layout="wide")

st.title("📊 Real-Time Stock Market Dashboard")

# Sidebar options
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Fetching data
@st.cache_data(ttl=60)
def load_data(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

data = load_data(symbol, start_date, end_date)

if data.empty:
    st.error("⚠️ No data found. Please check the symbol or date range.")
    st.stop()

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(data)

# Plot closing price
st.subheader(f"📈 Closing Price of {symbol}")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Close", line=dict(color='blue')))
fig.update_layout(title=f"{symbol} Closing Price", xaxis_title="Date", yaxis_title="Price (USD)", height=400)
st.plotly_chart(fig, use_container_width=True)

# Moving Averages
st.subheader("📉 Moving Averages")
ma1 = st.slider("MA Window 1", min_value=5, max_value=50, value=10)
ma2 = st.slider("MA Window 2", min_value=10, max_value=100, value=20)

data['MA1'] = data['Close'].rolling(window=ma1).mean()
data['MA2'] = data['Close'].rolling(window=ma2).mean()

fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Close", line=dict(color='lightgray')))
fig_ma.add_trace(go.Scatter(x=data.index, y=data['MA1'], name=f"MA {ma1}", line=dict(color='green')))
fig_ma.add_trace(go.Scatter(x=data.index, y=data['MA2'], name=f"MA {ma2}", line=dict(color='red')))
fig_ma.update_layout(title=f"{symbol} Moving Averages", xaxis_title="Date", yaxis_title="Price", height=400)
st.plotly_chart(fig_ma, use_container_width=True)

# Volume chart
st.subheader("📦 Volume Traded")
fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"))
fig_vol.update_layout(title=f"{symbol} Volume", xaxis_title="Date", yaxis_title="Shares Traded", height=300)
st.plotly_chart(fig_vol, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Built with Python, Streamlit, Plotly, and yfinance API")
