import streamlit as st
from components import state, data_loader, ui


# region Page config
st.set_page_config(
    page_title="Lapage Dashboard",
    page_icon="📚",
    layout='wide'
)

st.title("📚 Analyse des ventes Lapage")
st.markdown("Bienvenue sur le dashboard interactif de Lapage.")
st.markdown("""
📌 Pages disponibles :

- **KPIs** → analyse détaillée des performances  
- **Evolution du CA** → tendances dans le temps  
- **Corrélations** → relations entre variables 
            
👉 Utilisez les filtres à gauche pour explorer les données.
""")

# Load session state and data
state.init_state()
ui.make_sidebar(show_categ=False, show_date=False)

# region View

kpis = data_loader.get_basic_kpis(
    segment=st.session_state.get("selected_segment_value"),
    sex=st.session_state.get("selected_sex_value")
)
col1, col2, col3, col4 = st.columns(4)

if kpis:
    col1.metric("💰 CA total", f"{kpis['ca_total']:,.0f} €", border=True)
    col2.metric("👥 Clients uniques", f"{kpis['nb_clients']:,}", border=True)
    col3.metric("🛒 Transactions", f"{kpis['transactions']:,}", border=True)
    col4.metric("📦 Panier moyen", f"{kpis['panier_moyen']:,.2f} €", border=True)
else:
    df = data_loader.get_filtered_df()

    col1.metric("Transactions", f"{len(df):,}", border=True)
    col2.metric("Clients actifs", f"{df['client_id'].nunique():,}", border=True)
    col3.metric("Produits actifs", f"{df['id_prod'].nunique():,}", border=True)
    col4.metric("Période", "24 mois", border=True)