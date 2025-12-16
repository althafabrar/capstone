# logic/compute.py
def summary_stats(df):
    # df kolom: id,no_pesanan,pesanan,jumlah,omzet,catatan,bulan (lowercase)
    return {
        "total_pesanan": int(df["id"].nunique()) if "id" in df.columns else 0,
        "total_jumlah": int(df["jumlah"].sum()) if "jumlah" in df.columns else 0,
        "total_omzet": float(df["omzet"].sum()) if "omzet" in df.columns else 0.0
    }
