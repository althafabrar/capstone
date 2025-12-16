# logic/connection.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Kembalikan koneksi MySQL. Jika gagal, kembalikan None.
    Sesuaikan host/user/password/database jika perlu.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",      # jika ada password, ganti di sini
            database="capstone",
            autocommit=False
        )
        return conn
    except Error as e:
        # print ke terminal agar mudah debugging
        print("MySQL connection error:", e)
        return None
