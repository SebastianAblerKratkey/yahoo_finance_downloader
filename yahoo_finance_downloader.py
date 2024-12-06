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

if ticker:
    ticker = ticker.strip().upper()  # Clean input
    st.write(f"Fetching data for: {ticker}...")
    try:
        # Download maximum available historical data
        data = yf.download(ticker, period="max")
        data.reset_index(inplace=True)
        
        # Display the entire dataset
        st.write(f"Data for {ticker}:")
        st.dataframe(data)
        
        # Generate download link with filename as the ticker
        filename = f"{ticker}.xlsx"
        generate_excel_download_link(data, filename=filename)
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
