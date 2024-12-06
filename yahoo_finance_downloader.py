import pandas as pd
from io import BytesIO
import base64
import streamlit as st
import yfinance as yf

# Function to generate Excel download link (unchanged)
def generate_excel_download_link(df, filename="template.xlsx"):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{filename}</a>'
    return st.markdown(href, unsafe_allow_html=True)

# Streamlit App
st.header("Yahoo Finance Data Downloader")

# Input for tickers
input_tickers = st.text_input(
    "Enter Yahoo Finance tickers of the assets (separated by commas):",
    help="Example: AAPL, MSFT, TSLA"
)

if input_tickers:
    # Parse and clean tickers
    tickers = [ticker.strip().upper() for ticker in input_tickers.split(",")]

    # Process each ticker individually
    for ticker in tickers:
        st.write(f"Fetching data for: {ticker}...")
        try:
            # Download maximum available historical data
            data = yf.download(ticker, period="max")
            data.reset_index(inplace=True)
            data["Ticker"] = ticker  # Add a column for the ticker symbol
            
            # Display a preview of the data
            st.write(f"Data for {ticker}:", data.head())
            
            # Generate download link with filename as the ticker
            filename = f"{ticker}.xlsx"
            generate_excel_download_link(data, filename=filename)
        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}: {e}")
