import streamlit as st
import pandas as pd
from components.data_loader import get_filtered_df

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src import ca_moyenne_mobile, test_statistic

def panier_moyen_per_session() -> float:
    df = get_filtered_df()
    sessions = df.groupby('session_id')['price'].sum()
    return sessions.mean()


def panier_moyen_per_client() -> float:
    df = get_filtered_df()
    clients = df.groupby('client_id')['price'].sum()
    return clients.mean()


def ca_per_categ():
    df = get_filtered_df()
    return df.groupby('categ')['price'].sum().reset_index()


def ca_per_client(categ_list = [0, 1, 2]):
    df = get_filtered_df()
    df = df.groupby(['client_id', 'categ'])['price'].sum().unstack().reset_index()
    df['sum'] = df[categ_list].sum(axis=1)
    df.sort_values(by='sum', ascending=False, inplace=True)
    return df.iloc[:, :len(categ_list) + 1]


def ca_per_product(categ_list = [0, 1, 2]):
    df = get_filtered_df()
    df = df.groupby(['id_prod', 'categ'])['price'].sum().unstack().reset_index()
    df['sum'] = df[categ_list].sum(axis=1)
    df.sort_values(by='sum', ascending=False, inplace=True)
    return df.iloc[:, :len(categ_list) + 1]


def ca_mm(freq='D', rolling=[7]):
    df = get_filtered_df()
    freq = 'ME' if freq == 'M' else freq
    return ca_moyenne_mobile(df, 'price', freq, rolling)


# region Metrics for KPIs page

def get_comparison_metrics():
    df = st.session_state.df
    df_temp = df.copy()

    cut = df_temp['date'].min() + pd.DateOffset(months=12)

    df_y1 = df_temp[df_temp['date'] < cut]
    df_y2 = df_temp[df_temp['date'] >= cut]

    def delta(new, old):
        if old == 0:
            return 0
        return (new - old) / old * 100
    
    return {
        # CA
        "ca_y2": df_y2['price'].sum(),
        "ca_delta": delta(df_y2['price'].sum(), df_y1['price'].sum()),

        # Clients
        "clients_y2": df_y2['client_id'].nunique(),
        "clients_delta": delta(df_y2['client_id'].nunique(), df_y1['client_id'].nunique()),

        # Commandes / client
        "orders_per_client_y2": df_y2['session_id'].nunique() / df_y2['client_id'].nunique(),
        'orders_per_client_delta': delta(
            df_y2['session_id'].nunique() / df_y2['client_id'].nunique(), 
            df_y1['session_id'].nunique() / df_y1['client_id'].nunique()
        ),

        # Prix moyen produit
        "avg_price_y2": df_y2['price'].mean(),
        "avg_price_delta": delta(df_y2['price'].mean(), df_y1['price'].mean()),

        # Panier moyen / session
        "basket_y2": df_y2.groupby('session_id')['price'].sum().mean(),
        "basket_delta": delta(
            df_y2.groupby('session_id')['price'].sum().mean(),
            df_y1.groupby('session_id')['price'].sum().mean()
        ),

        # B2B vs B2C by CA
        "b2b_y2": df_y2[df_y2['segment_client'] == 'B2B']['price'].sum() / df_y2['price'].sum() * 100,
        "b2b_delta": delta(
            df_y2[df_y2['segment_client'] == 'B2B']['price'].sum() / df_y2['price'].sum(),
            df_y1[df_y1['segment_client'] == 'B2B']['price'].sum() / df_y1['price'].sum() 
        ),

        # Catégorie
        "top_categ_y2": df_y2.groupby('categ')['price'].sum().idxmax(),
        "top_categ_delta": delta(
            df_y2[df_y2['categ'] == df_y2.groupby('categ')['price'].sum().idxmax()]['price'].sum(),
            df_y1[df_y1['categ'] == df_y2.groupby('categ')['price'].sum().idxmax()]['price'].sum()
        ),

        # Produits vendus
        "prod_sold_y2": df_y2['id_prod'].nunique(),
        "prod_sold_delta": delta(
            df_y2['id_prod'].nunique(),
            df_y1['id_prod'].nunique()
        )
    }

# region Stats

# calculation.py
def interpret_lorenz(gini) -> dict:
    # Text interpretation
    if gini < 0.2:
        level = "très faible"
        emoji = "🟢"
        detail = "Les revenus sont très bien répartis entre les clients."
    elif gini < 0.4:
        level = "modérée"
        emoji = "🟡"
        detail = "Une légère concentration des revenus sur certains clients."
    elif gini < 0.6:
        level = "forte"
        emoji = "🟠"
        detail = "Une minorité de clients génère une grande part du CA."
    else:
        level = "très forte"
        emoji = "🔴"
        detail = "Le CA est très concentré sur quelques clients clés."

    return {
        "level": level,
        "emoji": emoji,
        "detail": detail
    }

def corr_list():
    return {
        "Âge": "age", 
        "Genre": "sex",
        "Catégorie": "categ",
        "Montant total": "montant_total",
        "Fréquence d’achat": "freq",
        "Panier moyen": "panier_moyen"
    }

def test_stats(df: pd.DataFrame, col1: str, col2: str, alpha=0.05):
    return test_statistic(
        df=df,
        col1=col1,
        col2=col2,
        alpha=alpha
    )

def get_corr_df(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    CLIENT_VARS = {"age", "sex"}
    AGG_VARS = {"montant_total", "freq", "panier_moyen"}
    TRANSACTION_VARS = {"categ"}

    df_client = df.groupby('client_id').agg(
        age=('age', 'mean'),
        sex=('sex', 'first'),
        montant_total=('price', 'sum'),
        freq=('session_id', 'nunique'),
        panier_moyen=('price', 'mean')
    ).reset_index()

    df_client.age = df_client.age.round(0).astype(int)
    df_transaction = df.copy()

    if col1 not in TRANSACTION_VARS and col2 not in TRANSACTION_VARS:
        return df_client[[col1, col2]]
    elif col1 in TRANSACTION_VARS or col2 in TRANSACTION_VARS:
        if col1 in CLIENT_VARS or col2 in CLIENT_VARS:
            return df[[col1, col2]]
        else:
            df_transaction = df.copy()
            cols = ['client_id']

            if col1 in AGG_VARS:
                cols.append(col1)
                
            if col2 in AGG_VARS:
                cols.append(col2)
            
            df_transaction = df_transaction.merge(
                df_client[cols],
                on='client_id',
                how='left'
            )
            return df_transaction[[col1, col2]]