import streamlit as st
from components import state, data_loader, calculation, ui, graph_plotly

# region Setup
st.set_page_config(layout="wide")
st.title("🌏 Évolution du chiffre d'affaires")
st.markdown("""
    > **Évolution du chiffre d'affaires** avec moyenne mobile.  
    > Sélectionnez une granularité **(Jour / Mois)** et une ou plusieurs **périodes de lissage** pour visualiser les tendances.
""")
st.divider()

state.init_state()
ui.make_sidebar()
df = data_loader.get_filtered_df()

# region Control
col1, col2, _ = st.columns([1, 2, 2])
value_unit = col1.radio(
    "Granularité",
    ['Jour', 'Mois']
)
# value_duration
value_period = col2.multiselect(
    "Périodes (moyenne mobile)",
    options=[2, 3, 7, 14, 30, 60, 90],
    default=[7],
    max_selections=3,
    format_func=lambda x: f"{x} {'Jours' if value_unit == 'Jour' else 'Mois'}"
)

# region Graph
df_mm = calculation.ca_mm(
    'ME' if value_unit == 'Mois' else 'D', 
    value_period
)
fig = graph_plotly.plot_line_plotly(
    df_mm,
    'date',
    df_mm.columns[1:]
)
st.plotly_chart(
    fig,
    width='stretch'
)