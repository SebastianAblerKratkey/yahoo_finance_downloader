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

# Input for single ticker
ticker = st.text_input(
    "Enter a Yahoo Finance ticker:",
    help="Example: AAPL"
)

# Dropdown for frequency selection
interval = st.selectbox(
    "Select data frequency:",
    options=["Daily", "Monthly"],
    index=0,  # Default to Daily
    help="Choose 'Daily' for daily data or 'Monthly' for monthly aggregated data."
)

# Map interval selection to yfinance interval parameter
interval_map = {
    "Daily": "1d",
    "Monthly": "1mo"
}
selected_interval = interval_map[interval]

if ticker:
    ticker = ticker.strip().upper()  # Clean input
    st.write(f"Fetching {interval.lower()} price data for: {ticker}...")
    try:
        # Download maximum available historical data with the chosen interval
        data = yf.download(ticker, period="max", interval=selected_interval)
        data.reset_index(inplace=True)
        
        if data.empty:
            st.error(f"Ticker '{ticker}' could not be found.")
        else:
            # Display the dataset
            st.write(f"{interval} price data for {ticker}:")
            st.dataframe(data)
            
            # Generate download link with filename as the ticker
            filename = f"{ticker}_{interval.lower()}.xlsx"
            generate_excel_download_link(data, filename=filename)
    except Exception as e:
        st.error(f"An error occurred while fetching data for ticker '{ticker}': {e}")
