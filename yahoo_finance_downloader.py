import pandas as pd
from io import BytesIO
import base64
import streamlit as st
import yfinance as yf

# Function to generate Excel download link (unchanged)
def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="template.xlsx">Excel template'
    return st.markdown(href, unsafe_allow_html=True)

# Streamlit App
st.header("Yahoo Finance Stock Price Downloader")

# Input for stock tickers
input_tickers = st.text_input(
    "Enter the Yahoo Finance tickers of the assets (separated by commas):",
    help="Example: AAPL, MSFT, TSLA"
)

if input_tickers:
    # Parse and clean tickers
    tickers = [ticker.strip().upper() for ticker in input_tickers.split(",")]

    # Fetch data
    st.write(f"Fetching data for: {', '.join(tickers)}...")
    dataframes = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, period="1y")  # Fetch data for the past year
            data.reset_index(inplace=True)
            data["Ticker"] = ticker  # Add a column for the ticker symbol
            dataframes.append(data)
        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}: {e}")

    # Combine all data into a single DataFrame
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        st.write("Stock data preview:", combined_df.head())

        # Generate download link using the provided function
        generate_excel_download_link(combined_df)
    else:
        st.warning("No data to display or download.")
