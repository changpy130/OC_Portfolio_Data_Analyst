import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# CONFIGURATION DE LA PAGE
# ============================================

st.set_page_config(
    page_title="Dashboard BottleNeck",
    page_icon="🍷",
    layout="wide"
)

st.title("🍷 Dashboard BottleNeck")
st.markdown("*Analyse des ventes - Période : 10/2020*")

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================

# @st.cache_data
def gatData():
    df = pd.read_excel("files/df_merge.xlsx")
    return df

# Charger les données
df = gatData()

# ============================================
# SIDEBAR - FILTRES
# ============================================
st.sidebar.header("🔍 Filtres")

# status of stock
statut = st.sidebar.selectbox("Statut stock", ["Tous", "In stock", "Out of stock"])

match statut:
    case 'In stock':
        df = df.loc[df.stock_status_clean == 'instock']
    case 'Out of stock':
        df = df.loc[df.stock_status_clean == 'outofstock']
    case 'Tous':
        pass

# product types
df.product_type.fillna('Inconnu', inplace=True)
product_type = st.sidebar.selectbox('Type de produit', ['Tous'] + df.product_type.unique().tolist())

if product_type != 'Tous':
    df = df.loc[df.product_type == product_type]

# ============================================
# SECTION 1 - KPIs
# ============================================

# Calculs : CA
df['ca'] = df.price * df.total_sales
ca_total = df.ca.sum()

# Calculs : nb produits
nb_produits = len(df.product_id)

# Calculs : Marge moyenne
marge_moyenne = (df.taux_marge.mean() * 100).round(2)

# Calculs : produits en rupture(nb)
nb_outofstock = len(df.loc[df.stock_status_clean == 'outofstock'])

# UI
st.header("📊 Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="CA Total", value=f"{ca_total:,.2f} €")
with col2:
    st.metric(label="Nb Produits", value=f"{nb_produits}")
with col3:
    st.metric(label="Marge Moyenne", value=f"{marge_moyenne} %")
with col4:
    st.metric(label="Nb Produits en Rupture", value=f"{nb_outofstock}")

# ============================================
# SECTION 2 - GRAPHIQUE CA
# ============================================
st.header("🏆 Top 10 produits par CA")

df_top_ca = df.sort_values('ca', ascending=False).head(10)
df_top_ca['label'] = (
    df_top_ca['product_id'].astype(str)
    + " ("
    + df_top_ca['product_type']
    + ")"
)
df_top_ca['ca_rounded'] = df_top_ca.ca.round(2)
df_top_ca = df_top_ca.sort_values('ca', ascending=True).reset_index(drop=True)
fig = px.bar(
    df_top_ca,
    x='ca_rounded',
    y='label',
    orientation='h',
    text='ca_rounded',
    color='product_type',
    color_discrete_sequence=px.colors.qualitative.Plotly,
    labels={
        'ca_rounded': 'Chiffre d’affaires (€)',
        'label': 'Produit',
        'product_type': 'Type de produit',
        'total_sales': 'Ventes'
    },
    hover_data={
        'total_sales': True,
        'label': False
    },
    height=500
)
fig.update_traces(
    texttemplate='%{text:,.0f} €',
    textposition='outside'
)
# to sort values (by total CA); if not, it's sorted inside the group(product_type)
fig.update_layout(
    yaxis=dict(categoryorder='total ascending')
)
st.plotly_chart(fig, width='stretch')

# ============================================
# SECTION 3 - STOCKS
# ============================================
st.header("📦 État des stocks")

# Donut chart for Instock vs. Outofstock
df_stock_par_statut = df.groupby('stock_status_clean').size().reset_index()
df_stock_par_statut.rename(columns={0: 'count'}, inplace=True)
fig = px.pie(
    df_stock_par_statut,
    names='stock_status_clean',
    color='stock_status_clean',
    color_discrete_sequence=px.colors.qualitative.T10,
    values='count',
    hole=0.5,
    labels={
        'stock_status_clean': 'Statut de stock'
    }
)
fig.update_traces(
    texttemplate='%{percent:.0%}'
)
st.plotly_chart(fig, width='stretch')

# stock_quantity by product_type
df_stock_par_type = df.groupby('product_type')['stock_quantity'].sum().reset_index()
df_stock_par_type = df_stock_par_type.sort_values('stock_quantity', ascending=False).reset_index(drop=True)

total_stock = df_stock_par_type['stock_quantity'].sum()
df_stock_par_type['Pourcentage'] = (
    df_stock_par_type['stock_quantity'] / total_stock * 100
).round(2).astype(str) + " %"

df_stock_par_type.rename(
    columns={'product_type': 'Type de produit', 'stock_quantity': 'Quantité de stock'},
    inplace=True
)
st.dataframe(df_stock_par_type)