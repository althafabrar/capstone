# main.py
import streamlit as st
import plotly.express as px
import pandas as pd  
import os
import uuid
import datetime

from logic.loader import load_data_sql
from logic.filter import filter_df
from logic.compute import summary_stats
from logic.sorter import sort_bulan
from logic import crud
from logic.config import load_config, save_config


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dashboard Rekap",
    layout="wide",
)

# --- CSS ---
st.markdown("""
<style>
/* Overall app background */
.stApp {
    background-color: #121212;
    color: #e0e0e0;
}

/* Metric cards style */
.metric-card {
    background-color: #1f1f1f;
    padding: 20px 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    color: #ffffff;
    margin-bottom: 20px;
}

/* Section title inside card */
.section-title {
    font-size: 22px !important;
    font-weight: bold;
    margin-top: 0px;
    margin-bottom: 15px;
    color: #ffffff !important;
}

/* Table */
.stDataFrame table {
    color: #e0e0e0;
    background-color: #1f1f1f;
}

/* Optional: scrollbar for long tables */
.stDataFrame div[data-testid="stVerticalBlock"] {
    max-height: 400px;
    overflow-y: auto;
}

.katalog-card {
    background: #1f1f1f;
    border-radius: 18px;
    padding: 14px;
    border: 1px solid #2a2a2a;
    transition: all 0.25s ease;
    height: 100%;

    display: flex;
    flex-direction: column;
}

.katalog-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.45);
}

/* WRAPPER GAMBAR */
.katalog-image-wrapper {
    width: 100%;
    height: 200px;
    overflow: hidden;
    border-radius: 14px;
    margin-bottom: 12px;
}

/* GAMBAR */
.katalog-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* BODY CARD */
.katalog-body {
    flex-grow: 1;
}

.katalog-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
}

.katalog-info {
    font-size: 13px;
    color: #b5b5b5;
    line-height: 1.5;
}

.katalog-desc {
    font-size: 13px;
    color: #d0d0d0;
    margin-top: 6px;
    max-height: 40px;
    overflow: hidden;
}

/* BUTTON AREA */
.katalog-btn {
    margin-top: 14px;
}

/* Bikin gambar katalog seragam */
[data-testid="stImage"] img {
    height: 300px;
    object-fit: cover;
    border-radius: 14px;
}


</style>
""", unsafe_allow_html=True)

config = load_config()

for key, val in config.items():
    if key not in st.session_state:
        # CASE 1: schedule_time disimpan sebagai string "HH:MM"
        if key == "schedule_time" and isinstance(val, str):
            try:
                h, m = map(int, val.split(":"))
                st.session_state.schedule_time = datetime.time(h, m)
            except Exception:
                st.session_state.schedule_time = datetime.time(8, 0)

        # CASE 2: nilai lain (bool, str, list)
        else:
            st.session_state[key] = val


# --- Top menu ---
from streamlit_option_menu import option_menu
selected = option_menu(
    menu_title=None,
    options=["Dashboard","Data Pesanan","Katalog","Pengaturan"],
    icons=["bar-chart","table","file-earmark-pdf","gear"],
    orientation="horizontal"
)

# --- Load Data ---
df = load_data_sql()
df = sort_bulan(df)

if st.session_state.notif_enabled:
    st.info(f"🔔 Notifikasi aktif ({st.session_state.notif_method})")

if st.session_state.schedule_on:
    st.success(
        f"⏱️ Laporan dijadwalkan {st.session_state.schedule_type} "
        f"pukul {st.session_state.schedule_time}"
    )

if st.session_state.theme_choice == "Light Mode":
    st.markdown("<style>.stApp{background:#fafafa;color:#000}</style>", unsafe_allow_html=True)


if selected == "Dashboard":
    st.title("📊 Dashboard Rekap")
    
    # --- Stats Summary ---
    stats = summary_stats(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pesanan", stats["total_pesanan"])
    c2.metric("Total Jumlah Produk", f"{stats['total_jumlah']:,}")
    c3.metric("Total Omzet (Rp)", f"{stats['total_omzet']:,.0f}")
    
    st.markdown("---")
    
    # --- Filter Data ---
    bulan_filter = st.multiselect(
        "Filter Bulan",
        options=list(df["bulan"].unique()) if "bulan" in df.columns else [],
        default=list(df["bulan"].unique()) if "bulan" in df.columns else []
    )
    df_filtered = filter_df(df, bulan_filter) if bulan_filter else df
    df_filtered = sort_bulan(df_filtered)
    
    # --- Prepare Chart Data ---
    fig_omzet = df_filtered.groupby("bulan", as_index=False)["omzet"].sum()
    fig_jumlah = df_filtered.groupby("bulan", as_index=False)["jumlah"].sum()
    
    # --- Grafik Omzet & Jumlah Produk side by side ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='metric-card'><p class='section-title'>📈 Grafik Omzet per Bulan</p></div>", unsafe_allow_html=True)
        fig1 = px.line(
            sort_bulan(fig_omzet, "bulan"),
            x="bulan",
            y="omzet",
            markers=True
        )
        fig1.update_traces(
            line=dict(color='#4B0082', width=3),
            marker=dict(size=8, color='#4B0082')
        )
        fig1.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='#1f1f1f',
            paper_bgcolor='#1f1f1f',
            font=dict(color='white'),
            xaxis=dict(color='white', gridcolor='gray'),
            yaxis=dict(color='white', gridcolor='gray'),
            title_font=dict(size=18, color='white')
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("<div class='metric-card'><p class='section-title'>📊 Grafik Jumlah Produk</p></div>", unsafe_allow_html=True)
        fig2 = px.bar(
            sort_bulan(fig_jumlah, "bulan"),
            x="bulan",
            y="jumlah",
            color_discrete_sequence=['#4B0082']
        )
        fig2.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='#1f1f1f',
            paper_bgcolor='#1f1f1f',
            font=dict(color='white'),
            xaxis=dict(color='white', gridcolor='gray'),
            yaxis=dict(color='white', gridcolor='gray'),
            title_font=dict(size=18, color='white')
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # --- Pie Chart & Data Tersaring side by side ---
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("<div class='metric-card'><p class='section-title'>🧩 Proporsi Omzet</p></div>", unsafe_allow_html=True)
        fig3 = px.pie(
            df_filtered,
            names="bulan",
            values="omzet",
            color_discrete_sequence=px.colors.sequential.Purples
        )
        fig3.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='#1f1f1f',
            paper_bgcolor='#1f1f1f',
            font=dict(color='white'),
            title_font=dict(size=18, color='white')
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <p class='section-title'>📄 Data Tersaring</p>
        </div>
        """, unsafe_allow_html=True)

        if df_filtered.empty:
            st.warning("Data tidak ditemukan sesuai filter yang dipilih")
        else:
            st.dataframe(df_filtered, use_container_width=True)

    
elif selected == "Data Pesanan":
    st.title("📦 Kelola Data Pesanan")
    df = load_data_sql()
    df = sort_bulan(df)
    
    st.subheader("Data Pesanan")
    st.dataframe(df, use_container_width=True)
    
    # TAMBAH DATA
    st.markdown("---")
    st.subheader("➕ Tambah Pesanan")
    with st.form("add_form", clear_on_submit=True):
        no_pesanan = st.text_input("No Pesanan")
        pesanan = st.text_input("Pesanan")
        jumlah = st.number_input("Jumlah", min_value=0)
        omzet = st.number_input("Omzet", min_value=0)
        catatan = st.text_input("Catatan")
        bulan = st.selectbox("Bulan", [
            "Januari","Februari","Maret","April","Mei","Juni","Juli",
            "Agustus","September","Oktober","November","Desember"
        ])
        submit = st.form_submit_button("Simpan")
    
    if submit:
        try:
            crud.insert_data(no_pesanan, pesanan, jumlah, omzet, catatan, bulan)
            st.success("Data tersimpan ke database.")
            st.rerun()
        except Exception as e:
            st.error(f"Gagal menyimpan: {e}")
    
   # --- EDIT DATA (FINAL FIX) ---
    st.markdown("---")
    st.subheader("✏️ Edit / Hapus")
    df = load_data_sql()

    if df.empty:
        st.info("Tidak ada data.")
    else:
        ids = df["id"].tolist()
        colA, colB = st.columns(2)

        # =============================
        #     PERBAIKAN EDIT MODE
        # =============================
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False
            st.session_state.edit_id = None

        # ----------- EDIT ------------
        with colA:
            sel_id = st.selectbox("Pilih ID untuk Edit", ids)

            if st.button("✏️ Edit Mode"):
                st.session_state.edit_mode = True
                st.session_state.edit_id = sel_id
                st.rerun()

            # Jika tombol edit ditekan → tampilkan FORM EDIT
            if st.session_state.edit_mode and st.session_state.edit_id == sel_id:

                row = df[df["id"] == sel_id].iloc[0]

                with st.form("edit_form"):
                    no_pesanan2 = st.text_input("No Pesanan", value=row["no_pesanan"])
                    pesanan2 = st.text_input("Pesanan", value=row["pesanan"])
                    jumlah2 = st.number_input("Jumlah", min_value=0, value=int(row["jumlah"]))
                    omzet2 = st.number_input("Omzet", min_value=0, value=int(row["omzet"]))
                    catatan2 = st.text_input("Catatan", value=row["catatan"])

                    bulan_options = [
                        "Januari","Februari","Maret","April","Mei","Juni",
                        "Juli","Agustus","September","Oktober","November","Desember"
                    ]
                    bulan2 = st.selectbox(
                        "Bulan",
                        bulan_options,
                        index=bulan_options.index(row["bulan"]) if row["bulan"] in bulan_options else 0
                    )

                    ok = st.form_submit_button("Update")

                if ok:
                    crud.update_data(
                        sel_id,
                        no_pesanan2,
                        pesanan2,
                        jumlah2,
                        omzet2,
                        catatan2,
                        bulan2
                    )
                    st.success("✔ Data berhasil diperbarui!")

                    # reset state
                    st.session_state.edit_mode = False
                    st.session_state.edit_id = None
                    st.rerun()
                    
            # --- DELETE ---
            with colB:
                del_id = st.selectbox("Pilih ID untuk Hapus", ids, key="del")
                if st.button("🗑 Hapus"):
                    try:
                        crud.delete_data(del_id)
                        st.success("Terhapus.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal hapus: {e}")

        st.markdown("---")
        st.subheader("📤 Import Data Pesanan dari Excel/CSV")

        uploaded_file = st.file_uploader("Upload file Excel (.xlsx) atau CSV (.csv)", type=["xlsx","csv"])

        if uploaded_file is not None:
            try:
                # baca file sesuai ekstensi
                if uploaded_file.name.lower().endswith(".csv"):
                    df_excel = pd.read_csv(uploaded_file)
                else:
                    df_excel = pd.read_excel(uploaded_file)

                st.write("**Preview file** (5 baris pertama)")
                st.dataframe(df_excel.head(), use_container_width=True)

                required_cols = ["no_pesanan", "pesanan", "jumlah", "omzet", "catatan", "bulan"]

                # validasi kolom
                missing = [c for c in required_cols if c not in df_excel.columns]
                if missing:
                    st.error(f"Kolom berikut masih hilang: {missing}. Gunakan template atau ubah header kolom sesuai.")
                else:
                    # optional: konversi tipe
                    df_excel["jumlah"] = pd.to_numeric(df_excel["jumlah"], errors="coerce").fillna(0).astype(int)
                    df_excel["omzet"] = pd.to_numeric(df_excel["omzet"], errors="coerce").fillna(0).astype(float)
                    # bersihkan whitespace di kolom string
                    for c in ["no_pesanan","pesanan","catatan","bulan"]:
                        df_excel[c] = df_excel[c].astype(str).str.strip()

                    st.info(f"File valid — {len(df_excel)} baris siap diimport.")

                    # opsi untuk hindari duplikasi berdasarkan no_pesanan
                    dedup_option = st.checkbox("Abaikan baris dengan no_pesanan yang sudah ada di database", value=True)

                    if st.button("➡️ Import ke Database"):
                        inserted = 0
                        failed = 0
                        total = len(df_excel)

                        # ambil daftar existing no_pesanan bila dedup aktif
                        existing_nos = set()
                        if dedup_option:
                            try:
                                df_existing = load_data_sql()
                                existing_nos = set(df_existing["no_pesanan"].astype(str).tolist())
                            except Exception:
                                existing_nos = set()

                        with st.spinner("Mengimpor data..."):
                            progress = st.progress(0)
                            for i, row in df_excel.iterrows():
                                try:
                                    if dedup_option and str(row["no_pesanan"]) in existing_nos:
                                        # skip jika sudah ada
                                        failed += 1
                                    else:
                                        # panggil fungsi insert_data dari crud
                                        crud.insert_data(
                                            row["no_pesanan"],
                                            row["pesanan"],
                                            int(row["jumlah"]),
                                            float(row["omzet"]),
                                            row["catatan"],
                                            row["bulan"]
                                        )
                                        inserted += 1
                                except Exception as e:
                                    # catat gagal tapi lanjut
                                    failed += 1
                                    # optional: log error ke console
                                    print("Import row error:", e)
                                progress.progress(int((i+1)/total*100))

                        st.success(f"Import selesai — Berhasil: {inserted}, Dilewati/Gagal: {failed}")
                        st.rerun()

            except Exception as e:
                st.error(f"Gagal memproses file: {e}")
    
# KATALOG
elif selected == "Katalog":
    st.title("📘 Katalog Produk")

    UPLOAD_DIR = "images/produk"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    df_katalog = crud.load_katalog()

    # ---------- TAMBAH PRODUK ----------
    with st.expander("➕ Tambah Produk"):
        with st.form("add_katalog", clear_on_submit=True):
            nama = st.text_input("Nama Barang")
            size = st.text_input("Size")
            bahan = st.text_input("Bahan")
            ket = st.text_area("Keterangan")
            gambar = st.file_uploader("Upload Gambar", type=["jpg", "png"])
            submit = st.form_submit_button("Simpan")

        if submit:
            if not nama or gambar is None:
                st.warning("Nama dan gambar wajib diisi")
            else:
                filename = f"{uuid.uuid4().hex}_{gambar.name}"
                path = f"{UPLOAD_DIR}/{filename}"

                with open(path, "wb") as f:
                    f.write(gambar.getbuffer())

                crud.insert_katalog(nama, size, bahan, ket, path)
                st.success("Produk berhasil ditambahkan")
                st.rerun()

    st.markdown("---")

    # ---------- GRID PRODUK ----------
   # ---------- GRID PRODUK ----------
    if df_katalog.empty:
        st.info("Belum ada produk")
    else:
        cols = st.columns(3)

        for i, row in df_katalog.iterrows():
            with cols[i % 3]:
                st.markdown("<div class='katalog-card'>", unsafe_allow_html=True)

                # IMAGE (AMAN UNTUK STREAMLIT)
                if row["gambar"] and os.path.exists(row["gambar"]):
                    st.image(row["gambar"], use_container_width=True)
                else:
                    st.image(
                        "https://via.placeholder.com/400x300?text=No+Image",
                        use_container_width=True
                    )

                # BODY
                st.markdown(
                    f"<div class='katalog-title'>{row['nama_barang']}</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class='katalog-info'>
                        📐 Size: {row['size']} <br>
                        🧵 Bahan: {row['bahan']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<div class='katalog-desc'>{row['keterangan']}</div>",
                    unsafe_allow_html=True
                )

                # BUTTON
                if st.button("✏️ Edit Produk", key=f"edit_{row['id']}"):
                    st.session_state.edit_katalog = int(row["id"])

                st.markdown("</div>", unsafe_allow_html=True)

    # ---------- EDIT MODE ----------
    if "edit_katalog" in st.session_state:
        row = df_katalog[df_katalog["id"] == st.session_state.edit_katalog].iloc[0]
        st.markdown("---")
        st.subheader("✏️ Edit Produk")

        colA, colB = st.columns([1, 2])

        with colA:
            if row["gambar"] and os.path.exists(row["gambar"]):
                st.image(row["gambar"], use_container_width=True)

        with colB:
            with st.form("edit_produk"):
                nama2 = st.text_input("Nama", row["nama_barang"])
                size2 = st.text_input("Size", row["size"])
                bahan2 = st.text_input("Bahan", row["bahan"])
                ket2 = st.text_area("Keterangan", row["keterangan"])
                gambar2 = st.file_uploader("Ganti Gambar", type=["jpg", "png"])

                c1, c2 = st.columns(2)
                update = c1.form_submit_button("Update")
                delete = c2.form_submit_button("Hapus")

            if update:
                if gambar2:
                    filename = f"{uuid.uuid4().hex}_{gambar2.name}"
                    new_path = f"{UPLOAD_DIR}/{filename}"
                    with open(new_path, "wb") as f:
                        f.write(gambar2.getbuffer())
                else:
                    new_path = row["gambar"]

                crud.update_katalog(
                    int(row["id"]),
                    nama2, size2, bahan2, ket2, new_path
                )

                del st.session_state.edit_katalog
                st.success("Produk diperbarui")
                st.rerun()

            if delete:
                if row["gambar"] and os.path.exists(row["gambar"]):
                    os.remove(row["gambar"])

                crud.delete_katalog(int(row["id"]))
                del st.session_state.edit_katalog
                st.success("Produk dihapus")
                st.rerun()


# ===============================
# PENGATURAN
# ===============================
elif selected == "Pengaturan":
    from datetime import time

    st.title("⚙️ Pengaturan Sistem")

    # ===============================
    # INIT SESSION STATE (AMAN)
    # ===============================
    defaults = {
        "notif_enabled": True,
        "notif_method": "Email",
        "notif_priority": "Normal",
        "schedule_on": False,
        "schedule_type": "Harian",
        "schedule_time": time(8, 0),   # ⬅️ FIX UTAMA (tidak boleh None)
        "fav_products": [],
        "theme_choice": "Dark Grey (Default)"
    }

    for key, val in defaults.items():
        if key not in st.session_state or st.session_state[key] is None:
            st.session_state[key] = val

    # ===============================
    # CSS
    # ===============================
    st.markdown("""
        <style>
        .erp-card {
            background: #1e1e1e;
            padding: 25px;
            border-radius: 14px;
            border: 1px solid #2a2a2a;
            margin-bottom: 20px;
        }
        .erp-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #ffffff;
        }
        .erp-sub {
            font-size: 14px;
            color: #a1a1a1;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)

    # ===============================
    # NOTIFIKASI
    # ===============================
    with colA:
        st.markdown("<div class='erp-card'>", unsafe_allow_html=True)

        st.markdown("<div class='erp-title'>🔔 Notifikasi Sistem</div>", unsafe_allow_html=True)
        st.markdown("<div class='erp-sub'>Atur preferensi notifikasi sistem.</div>", unsafe_allow_html=True)

        st.session_state.notif_enabled = st.toggle(
            "Aktifkan Notifikasi",
            value=st.session_state.notif_enabled
        )

        st.session_state.notif_method = st.selectbox(
            "Metode Notifikasi",
            ["Email", "Popup Dashboard", "Keduanya"],
            index=["Email", "Popup Dashboard", "Keduanya"]
            .index(st.session_state.notif_method)
        )

        st.session_state.notif_priority = st.select_slider(
            "Prioritas Notifikasi",
            ["Rendah", "Normal", "Tinggi"],
            value=st.session_state.notif_priority
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ===============================
    # SCHEDULER
    # ===============================
    with colB:
        st.markdown("<div class='erp-card'>", unsafe_allow_html=True)

        st.markdown("<div class='erp-title'>⏱️ Penjadwalan Sistem</div>", unsafe_allow_html=True)
        st.markdown("<div class='erp-sub'>Pengingat otomatis laporan.</div>", unsafe_allow_html=True)

        st.session_state.schedule_on = st.toggle(
            "Aktifkan Scheduler Laporan",
            value=st.session_state.schedule_on
        )

        st.session_state.schedule_type = st.radio(
            "Frekuensi",
            ["Harian", "Mingguan", "Bulanan"],
            index=["Harian", "Mingguan", "Bulanan"]
            .index(st.session_state.schedule_type)
        )

        # ⬅️ FIX TIME INPUT (TIDAK ERROR)
        st.session_state.schedule_time = st.time_input(
            "Waktu Pengingat",
            value=st.session_state.schedule_time
        )

        st.markdown("</div>", unsafe_allow_html=True)

    colC, colD = st.columns(2)

    # ===============================
    # PRODUK FAVORIT
    # ===============================
    with colC:
        st.markdown("<div class='erp-card'>", unsafe_allow_html=True)

        st.markdown("<div class='erp-title'>⭐ Produk Favorit</div>", unsafe_allow_html=True)

        if "pesanan" in df.columns:
            st.session_state.fav_products = st.multiselect(
                "Pilih Produk Favorit",
                sorted(df["pesanan"].unique()),
                default=st.session_state.fav_products
            )
        else:
            st.info("Data produk belum tersedia.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ===============================
    # SAVE BUTTON (REAL & AMAN)
    # ===============================
    if st.button("💾 Simpan Semua Pengaturan", use_container_width=True):
        save_config({
            "notif_enabled": st.session_state.notif_enabled,
            "notif_method": st.session_state.notif_method,
            "notif_priority": st.session_state.notif_priority,
            "schedule_on": st.session_state.schedule_on,
            "schedule_type": st.session_state.schedule_type,
            "schedule_time": st.session_state.schedule_time.strftime("%H:%M"),
            "fav_products": st.session_state.fav_products,
            "theme_choice": st.session_state.theme_choice
        })
        st.success("Pengaturan berhasil disimpan!")
