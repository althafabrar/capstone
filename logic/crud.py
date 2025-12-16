# logic/crud.py
import pandas as pd
from logic.connection import get_connection

# =======================
# PESANAN CRUD
# =======================

def insert_data(no_pesanan, pesanan, jumlah, omzet, catatan, bulan):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("Tidak dapat terhubung ke database")

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO pesanan (no_pesanan, pesanan, jumlah, omzet, catatan, bulan)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (no_pesanan, pesanan, jumlah, omzet, catatan, bulan))
        conn.commit()
    finally:
        conn.close()


def update_data(id, no_pesanan, pesanan, jumlah, omzet, catatan, bulan):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE pesanan SET
            no_pesanan=%s,
            pesanan=%s,
            jumlah=%s,
            omzet=%s,
            catatan=%s,
            bulan=%s
        WHERE id=%s
    """
    cursor.execute(sql, (no_pesanan, pesanan, jumlah, omzet, catatan, bulan, id))
    conn.commit()
    conn.close()


def delete_data(id_val):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pesanan WHERE id=%s", (id_val,))
    conn.commit()
    conn.close()


# =======================
# KATALOG PRODUK CRUD
# =======================

def load_katalog():
    conn = get_connection()
    query = "SELECT * FROM katalog_produk ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =======================
# INSERT KATALOG
# =======================
def insert_katalog(nama, size, bahan, ket, gambar):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO katalog_produk 
        (nama_barang, size, bahan, keterangan, gambar)
        VALUES (%s, %s, %s, %s, %s)
    """, (nama, size, bahan, ket, gambar))

    conn.commit()
    conn.close()


# =======================
# UPDATE KATALOG
# =======================
def update_katalog(id_, nama, size, bahan, ket, gambar):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE katalog_produk
        SET nama_barang=%s, size=%s, bahan=%s, keterangan=%s, gambar=%s
        WHERE id=%s
    """, (nama, size, bahan, ket, gambar, int(id_)))  # ⬅️ CAST
    conn.commit()
    conn.close()



# =======================
# DELETE KATALOG
# =======================
def delete_katalog(id_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM katalog_produk WHERE id=%s",
        (int(id_),)   # ⬅️ CAST DI SINI
    )
    conn.commit()
    conn.close()