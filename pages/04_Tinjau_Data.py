import streamlit as st
import pandas as pd

from logic.loader import load_data

st.title("📋 Tinjau dan Export Data")

df = load_data()
st.dataframe(df)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Excel",
    csv,
    "rekap2024.csv",
    "text/csv"
)
