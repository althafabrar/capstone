import streamlit as st
import shutil
import os

st.title("⚙ Pengaturan Aplikasi")

logo = st.file_uploader("Upload Logo Baru (PNG)", type=["png"])

if logo:
    save_path = "assets/logo_moker.png"
    with open(save_path, "wb") as f:
        f.write(logo.read())
    st.success("✔ Logo berhasil diperbarui!")

st.info("Tema custom masih coming soon...")
