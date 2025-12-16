import streamlit as st
import os

def load_css():
    st.markdown("""
    <style>
    /* Sidebar dark theme */
    .sidebar .sidebar-content {
        background-color: #1f1f1f;
        color: #ffffff;
    }

    /* Overall app background */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }

    /* Metric cards */
    .metric-card {
        background-color: #1f1f1f;
        padding: 20px 25px;
        border-radius: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        text-align: center;
        border: 1px solid #333;
        color: #ffffff;
        margin-bottom: 0px;
    }

    /* Section title */
    .section-title {
        font-size: 22px !important;
        font-weight: bold;
        margin-top: 25px;
        color: #ffffff !important;
    }

    /* Table */
    .stDataFrame table {
        color: #e0e0e0;
        background-color: #1f1f1f;
    }
    </style>
    """, unsafe_allow_html=True)

def header():
    logo_path = "assets/katalog/logo_moker.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=150)
    st.markdown('<h1>📊 Dashboard Rekap</h1>', unsafe_allow_html=True)
