import pandas as pd
from pathlib import Path
import requests
import streamlit as st

# parent path
DATA_DIR = Path(__file__).parent.parent / "data"
API_URL = "http://localhost:8000"

# region Load final table
def load_file_joined() -> pd.DataFrame:
    """Load directly the joined DataFrame (customers + products + transactions)"""

    df_c =load_customers()
    df_p = load_products()
    df_t = load_transactions()

    df_final = pd.merge(
        left=df_t,
        right=df_c,
        on='client_id',
        how='left'
    )
    df_final = pd.merge(
        left=df_final,
        right=df_p,
        on='id_prod',
        how='left'
    )
    return df_final

def load_all_clients() -> pd.DataFrame:
    return load_file('processed/all_clients.csv', sep=',')

def load_b2b() -> pd.DataFrame:
    return load_file('processed/clients_b2b.csv', sep=',')

def load_b2c() -> pd.DataFrame:
    return load_file('processed/clients_b2c.csv', sep=',')

# region Load files (Private)
def load_customers() -> pd.DataFrame:
    return load_file('raw/customers.csv')

def load_products() -> pd.DataFrame:
    return load_file('raw/products.csv')

def load_transactions() -> pd.DataFrame:
    df = load_file('raw/transactions.csv')
    df.date = pd.to_datetime(df.date)
    return df

def show_info(df):
    print("shape:")
    print(df.shape)

    print("\n--------")
    print("info:")
    print(df.info())

    print("\n--------")
    print("unique values:")
    print(df.nunique())

    print("\n--------")
    print("head: ")
    print(df.head())

# region Utility functions (Private)
def load_file(file, sep=';') -> pd.DataFrame:
    return pd.read_csv(
        DATA_DIR / file, 
        sep=sep,
        low_memory=False
    ).dropna(how='all')


# region APIs

def get_basic_kpis(segment: str = None, sex: str = None):
    params = {}

    if segment:
        params['segment'] = segment
    if sex:
        params['sex'] = sex
    
    try:
        response = requests.get(f"{API_URL}/api/kpis", params=params, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API error: {response.status_code}")
            return None
        
    except requests.exceptions.ConnectionError:
        print("⚠️ ConnectionError from API")
        return None
    except requests.exceptions.ConnectTimeout:
        print("⚠️ ConnectTimeout from API")
        return None