# logic/sorter.py
bulan_order = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
    "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
    "September": 9, "Oktober": 10, "November": 11, "Desember": 12
}

def sort_bulan(df, col="bulan"):
    if col not in df.columns:
        return df
    df["_bulan_num"] = df[col].map(bulan_order)
    df = df.sort_values("_bulan_num")
    df = df.drop(columns=["_bulan_num"])
    return df
