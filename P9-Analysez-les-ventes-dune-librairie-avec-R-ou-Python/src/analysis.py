import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ca(df: pd.DataFrame, targetCol: str, amountCol: str) -> pd.DataFrame:
    """Calculate CA

    Args:
        df (DataFrame): target DataFrame
        targetCol (String): column name of target(by client/category etc)
        amountCol (String): column name of amount
    """
    return df.groupby(targetCol)[amountCol].sum().reset_index().sort_values(amountCol, ascending=False)


def ca_moyenne_mobile(df: pd.DataFrame, col_ca: str, freq='D', rolling=[7, 30]) -> pd.DataFrame:
    # freq='D' -> day : grouped by day from the date ; 'M' -> month
    df_ca = df.groupby(pd.Grouper(key='date', freq=freq))[col_ca].sum().reset_index()
    df_ca.columns = ['date', 'ca']

    for period in rolling:
        if period <= len(df_ca):  # 👈 avoid rolling window larger than data
            df_ca[f'mm_{period}'] = df_ca.ca.rolling(window=period).mean()
        else:
            print(f"Période {period} trop grande pour les données filtrées.")

    return df_ca
