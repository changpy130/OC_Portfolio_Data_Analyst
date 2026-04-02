import streamlit as st
from components import state, data_loader, calculation, ui, graph_plotly

# region Setup
st.set_page_config(layout='wide')
st.title("🧩 Corrélations")
st.markdown("""
> **Analyse des corrélations** sur le comportement des clients.  
> Sélectionnez deux variables pour visualiser leur relation et tester sa significativité statistique.
>
> | Variables | Test statistique | Interprétation |
> |---|---|---|
> | 2 numériques | Pearson / Spearman | Nuage de points + droite de tendance |
> | 1 numérique + 1 catégorielle | ANOVA | Boîte à moustaches |
> | 2 catégorielles | Chi-2 | Heatmap de contingence |
""")

state.init_state()
ui.make_sidebar()
df = data_loader.get_filtered_df()
df['categ'] = df['categ'].astype(str)

# region Control
st.divider()

list_corr = calculation.corr_list()

col1, col2, col3 = st.columns([2, 1, 2], vertical_alignment='center')
var1 = col1.selectbox(
    "Variable 1",
    options=list_corr.keys()
)

col2.markdown(
    "<p style='text-align: center; font-weight: bold; font-size: 1.2rem;'>VS</p>",
    unsafe_allow_html=True
)

var2 = col3.selectbox(
    "Variable 2",
    options=list_corr.keys(),
    index=2
)

if var1 == var2:
    st.warning("⚠️ Veuillez choisir deux variables différentes.")
    st.stop()

# region Graph

df_stats = calculation.get_corr_df(df, list_corr[var1], list_corr[var2])

st.subheader("🎸 Graphique")
st.plotly_chart(
    graph_plotly.plot_stats(
        df_stats,
        list_corr[var1],
        list_corr[var2]
    ),
    width='stretch'
)


# region Interpretation
st.subheader("🎰 Interprétation")

result = calculation.test_stats(
    df=df_stats,
    col1=list_corr[var1],
    col2=list_corr[var2]
)
st.text(result)