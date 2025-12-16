import tempfile
import os

def save_excel(df, path="data/rekap2024.xlsx"):
    tmpfd, tmppath = tempfile.mkstemp(suffix=".xlsx")
    os.close(tmpfd)

    df.to_excel(tmppath, index=False)
    os.replace(tmppath, path)
