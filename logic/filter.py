# logic/filter.py
def filter_df(df, bulan_list):
    if "bulan" not in df.columns:
        return df
    return df[df["bulan"].isin(bulan_list)]
