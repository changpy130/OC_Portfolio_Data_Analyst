import streamlit as st
from components import state, data_loader, calculation, ui, graph_plotly

# region Setup
st.set_page_config(layout='wide')
st.title("🌟 KPIs")

state.init_state()
ui.make_sidebar()

df = data_loader.get_filtered_df()

# region KPI cards

st.divider()
st.caption("📅 Année 2 vs Année 1 — comparaison indépendante des filtres")

df_metric = calculation.get_comparison_metrics()

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "💰 CA (an 2)", 
    f"{df_metric['ca_y2']:,.0f} €", 
    delta=f"{df_metric['ca_delta']:+.1f}%",
    border=True
)
col2.metric(
    "👥 Clients uniques (an 2)", 
    f"{df_metric['clients_y2']:,}",
    delta=f"{df_metric['clients_delta']:+.1f}%",
    border=True
)
col3.metric(
    "🔄 Commandes / client (an 2)", 
    f"{df_metric['orders_per_client_y2']:,.1f}", 
    delta=f"{df_metric['orders_per_client_delta']:+.1f}%",
    border=True
)
col4.metric(
    "💸 Prix moyen (an 2)", 
    f"{df_metric['avg_price_y2']:,.1f} €", 
    delta=f"{df_metric['avg_price_delta']:+.1f}%",
    border=True
)

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "🛒 Panier moyen / session (an 2)", 
    f"{df_metric['basket_y2']:,.1f} €", 
    delta=f"{df_metric['basket_delta']:+.1f}%",
    border=True
)
col2.metric(
    "📦 Part B2B (an 2)", 
    f"{df_metric['b2b_y2']:.2f} %",
    delta=f"{df_metric['b2b_delta']:+.1f}%",
    border=True
)
col3.metric(
    "🏆 Catégorie top",
    f"Catégorie {df_metric['top_categ_y2']}",
    delta=f"{df_metric['top_categ_delta']:+.1f} %",
    border=True
)
col4.metric(
    "📚 Produits vendus",
    f"{df_metric['prod_sold_y2']:,}",
    delta=f"{df_metric['prod_sold_delta']:+.1f} %",
    border=True
)

tab_client, tab_prod = st.tabs(["👤 Client", "📦 Produit"])

# region Section Client
categ_list = [st.session_state.selected_categ_value] if st.session_state.get("selected_categ_value") not in (None, "Tous") else [0, 1, 2]
# categ_list = st.session_state.selected_categ_value

with tab_client:
    st.subheader("Top 10 clients par CA")
    df_ca_client = calculation.ca_per_client(categ_list).head(10)
    st.plotly_chart(
        graph_plotly.plot_bar_plotly(
            df_ca_client, 
            col_x='client_id',
            col_y=categ_list,
            xlabel="Client ID",
            ylabel="CA",
            legendLabel="Catégorie"
        ),
        width='stretch'
    )

    fig, gini = graph_plotly.plot_lorenz_plotly(
        df,
        'client_id',
        'price'
    )
    result = calculation.interpret_lorenz(gini)

    st.subheader("Courbe de Lorenz")
    st.markdown(f"""
        > {result['emoji']} **Indice de Gini : {gini:.4f}** — Inégalité {result['level']}  
        > {result['detail']}
    """)

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.subheader("Répartition du CA total par catégorie")
    df_ca = calculation.ca_per_categ()
    st.plotly_chart(
        graph_plotly.plot_donut_plotly(
            df_ca.price,
            labels=[ "Catégorie " + str(x) for x in df_ca.categ]
        ),
        width='stretch'
    )

# region Section Product
with tab_prod:
    categ_list = list(map(int, categ_list))  # make sure it's integer

    st.subheader("Top 10 produits par CA")
    df_ca_prod = calculation.ca_per_product(categ_list).head(10)
    st.plotly_chart(
        graph_plotly.plot_bar_plotly(
            df_ca_prod, 
            col_x='id_prod',
            col_y=categ_list,
            xlabel="Produit ID",
            ylabel="CA",
            legendLabel="Catégorie"
        ),
        width='stretch'
    )

    st.divider()

    st.subheader("Positionnement des produits : CA vs Quantité")
    st.markdown(
        """
            - Les produits **Stars** (top CA et top quantité) appartiennent tous à la catégorie 1.
            - Les produits **Chers & Rares** génèrent un CA élevé malgré peu de ventes (prix unitaire élevé).
            - Les produits **Populaires & Pas Chers** nécessitent un volume important pour compenser leur faible marge.
        """
    )

    col1, _, _ = st.columns(3)
    value_rank = col1.select_slider("🏆 Taille du top", [5, 10, 15, 20])

    st.plotly_chart(
        graph_plotly.plot_product_positioning(
            st.session_state.df,
            value_rank
        ),
        width='stretch'
    )