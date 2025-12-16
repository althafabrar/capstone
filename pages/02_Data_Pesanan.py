import streamlit as st
from logic.loader import load_data
from logic.crud import insert_data, update_data, delete_data

st.title("📦 Kelola Data Pesanan")

df = load_data()

st.session_state.setdefault("edit_mode", False)
st.session_state.setdefault("edit_id", None)
# -------- EDIT MODE --------
if st.session_state.edit_mode:
    edit_id = st.session_state.edit_id
    row = df[df["id"] == edit_id].iloc[0]

    st.subheader(f"✏️ Edit Pesanan — ID {edit_id}")

    with st.form("edit_form"):

        col1, col2, col3 = st.columns(3)

        # === COL 1 ===
        with col1:
            no_pesanan = st.text_input("No Pesanan", value=row["no_pesanan"])
            pesanan = st.text_input("Pesanan", value=row["pesanan"])

        # === COL 2 ===
        with col2:
            jumlah = st.number_input("Jumlah", value=int(row["jumlah"]), min_value=0)
            omzet = st.number_input("Omzet", value=int(row["omzet"]), min_value=0)

        # === COL 3 ===
        with col3:
            catatan = st.text_input("Catatan", value=row["catatan"])
            bulan = st.selectbox(
                "Bulan",
                sorted(df["bulan"].unique()),
                index=sorted(df["bulan"].unique()).index(row["bulan"])
            )

        update_btn = st.form_submit_button("💾 Update")

    if update_btn:
        # kirim dengan field lengkap
        update_data(edit_id, pesanan, jumlah, omzet, catatan, bulan)

        st.success("✔ Data berhasil diperbarui")
        st.session_state.edit_mode = False
        st.session_state.edit_id = None
        st.rerun()

    st.markdown("---")


# -------- ADD MODE --------
if not st.session_state.edit_mode:

    st.subheader("➕ Tambah Pesanan")

    with st.form("add_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            no_pesanan = st.text_input("No Pesanan")
            pesanan = st.text_input("Pesanan")

        with col2:
            jumlah = st.number_input("Jumlah", min_value=0)
            omzet = st.number_input("Omzet", min_value=0)

        with col3:
            catatan = st.text_input("Catatan")
            bulan = st.selectbox("Bulan", sorted(df["bulan"].unique()))

        add_btn = st.form_submit_button("💾 Simpan")

    if add_btn:
        insert_data(no_pesanan, pesanan, jumlah, omzet, catatan, bulan)
        st.success("✔ Data berhasil ditambahkan")
        st.rerun()

# -------- TABLE --------
st.subheader("📋 Data Pesanan")
st.dataframe(df, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    edit_id = st.selectbox("Pilih ID Edit", df["id"])
    if st.button("✏️ Edit"):
        st.session_state.edit_id = edit_id
        st.session_state.edit_mode = True
        st.rerun()

with col2:
    del_id = st.selectbox("Pilih ID Delete", df["id"])
    if st.button("🗑 Hapus"):
        delete_data(del_id)
        st.success("✔ Data berhasil dihapus")
        st.rerun()
