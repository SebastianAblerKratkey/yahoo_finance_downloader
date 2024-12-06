import pandas as pd
import base64
from io import StringIO, BytesIO
import streamlit as st


def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="template.xlsx">Excel template'
    return st.markdown(href, unsafe_allow_html=True)

st.header("Yahoo Finance Downloader")

tickers = []
input_tickers = st.text_input("Enter the [Yahoo Finace](https://finance.yahoo.com) tickers of the assets you are interested in (seperated by comma). Make sure to select at least two.")
# [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)
if input_tickers:
    tickers  = input_tickers.split(",")
    tickers = [x.strip() for x in tickers]