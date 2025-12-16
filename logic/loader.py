# logic/loader.py
import pandas as pd
from logic.connection import get_connection

def load_data_sql():
    conn = get_connection()
    if conn is None:
        # kembalikan DataFrame kosong kolom yang diharapkan
        cols = ["id","no_pesanan","pesanan","jumlah","omzet","catatan","bulan"]
        return pd.DataFrame(columns=cols)
    try:
        query = "SELECT id, no_pesanan, pesanan, jumlah, omzet, catatan, bulan FROM pesanan"
        df = pd.read_sql(query, conn)
        conn.close()
        # normalize column names (lowercase)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        print("load_data_sql error:", e)
        if conn:
            conn.close()
        cols = ["id","no_pesanan","pesanan","jumlah","omzet","catatan","bulan"]
        return pd.DataFrame(columns=cols)
