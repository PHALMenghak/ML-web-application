import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Stock Price Viewer", page_icon="📈")

# Sidebar inputs
st.sidebar.header("User Input Options")
tickerSymbol = st.sidebar.text_input("Enter stock ticker", value="GOOGL", help="Example: AAPL, MSFT, TSLA")

start_date = st.sidebar.date_input("Start date", pd.to_datetime("2010-05-31"))
end_date = st.sidebar.date_input("End date", pd.to_datetime("2020-05-31"))

st.title("📈 Simple Stock Price App")
st.markdown(f"""
View historical **closing price** and **volume** for **{tickerSymbol.upper()}**  
From **{start_date}** to **{end_date}**
""")

# Fetch stock data
try:
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(start=start_date, end=end_date)

    if tickerDf.empty:
        st.error("No data found. Check the ticker symbol or date range.")
    else:
        # Show data
        st.subheader("Raw Data")
        st.write(tickerDf.tail())

        # Moving average
        tickerDf['MA30'] = tickerDf['Close'].rolling(window=30).mean()

        # Line chart with moving average
        st.subheader("Closing Price with 30-Day Moving Average")
        st.line_chart(tickerDf[['Close', 'MA30']])

        # Volume chart
        st.subheader("Volume Traded")
        st.line_chart(tickerDf['Volume'])

        # Optional: Candlestick chart
        st.subheader("Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(
            x=tickerDf.index,
            open=tickerDf['Open'],
            high=tickerDf['High'],
            low=tickerDf['Low'],
            close=tickerDf['Close']
        )])
        st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error fetching data: {e}")
