import streamlit as st
import base64
import os

st.title("📦 Katalog Produk Moker")

pdf_path = "assets/katalog/katalog_moker.pdf"

# ===== CEK FILE =====
if not os.path.exists(pdf_path):
    st.error("❌ File katalog tidak ditemukan di: assets/katalog/katalog_moker.pdf")
    st.stop()

# ===== BACA FILE =====
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

# ===== TOMBOL DOWNLOAD =====
st.download_button(
    label="📥 Download Katalog Produk (PDF)",
    data=pdf_bytes,
    file_name="katalog_moker.pdf",
    mime="application/pdf"
)

st.markdown("---")

# ===== IFRAME PDF VIEWER =====
pdf_display = f"""
<iframe 
    src="data:application/pdf;base64,{base64_pdf}"
    width="100%" height="800"
    style="border: none; border-radius: 10px;">
</iframe>
"""

st.markdown(pdf_display, unsafe_allow_html=True)
