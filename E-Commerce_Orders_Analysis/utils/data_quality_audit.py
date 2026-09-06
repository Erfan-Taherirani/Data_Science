import pandas as pd

def need_strip(series: pd.Series):
    return (series.str.strip() != series).sum()
