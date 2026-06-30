import streamlit as st
from components.sidebar import render_sidebar
from components.helper import show_pdf

render_sidebar()
st.title("📊 Tableaux de bord")
st.caption("Deux tableaux de bord réalisés sur Tableau : présentation du profil et veille métier.")

# region Dashboard
TABLEAU_W = 1366
TABLEAU_H = 795
TARGET_W  = 1000          # tweak to match your Streamlit column width
scale     = TARGET_W / TABLEAU_W
scaled_h  = int(TABLEAU_H * scale)   # ≈ 524 px

tableau_embed = f"""
<style>
  #outer {{
    width: {TARGET_W}px;
    height: {scaled_h}px;
    overflow: hidden;
  }}
  #inner {{
    width: {TABLEAU_W}px;
    transform: scale({scale:.4f});
    transform-origin: top left;
  }}
</style>

<div id="outer">
  <div id="inner">
    <div class='tableauPlaceholder' id='viz1782393808197' style='position:relative'>
      <noscript>
        <a href='#'>
          <img alt='Dashboard Profil'
               src='https://public.tableau.com/static/images/P1/P13_17821408267250/DashboardProfil/1_rss.png'
               style='border:none' />
        </a>
      </noscript>
      <object class='tableauViz' style='display:none;'>
        <param name='host_url'           value='https%3A%2F%2Fpublic.tableau.com%2F' />
        <param name='embed_code_version' value='3' />
        <param name='site_root'          value='' />
        <param name='name'               value='P13_17821408267250/DashboardProfil' />
        <param name='tabs'               value='no' />
        <param name='toolbar'            value='yes' />
        <param name='static_image'       value='https://public.tableau.com/static/images/P1/P13_17821408267250/DashboardProfil/1.png' />
        <param name='animate_transition' value='yes' />
        <param name='display_static_image' value='yes' />
        <param name='display_spinner'    value='yes' />
        <param name='display_overlay'    value='yes' />
        <param name='display_count'      value='yes' />
        <param name='language'           value='fr-FR' />
      </object>
    </div>
    <script type='text/javascript'>
      var divElement  = document.getElementById('viz1782393808197');
      var vizElement  = divElement.getElementsByTagName('object')[0];
      vizElement.style.width  = '{TABLEAU_W}px';
      vizElement.style.height = '{TABLEAU_H}px';
      var scriptElement = document.createElement('script');
      scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
      vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
  </div>
</div>
"""

st.iframe(tableau_embed, height=scaled_h + 60)

tab1, tab2 = st.tabs(["Profil", "Veille métier"])

# region Tab Veille
with tab2:
    st.subheader("🔍 Contenu de la veille")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🛠️ Outils testés**")

        outils = [
            ("Streamlit",   "Application data interactive en Python — utilisé pour ce portfolio"),
            ("FastAPI",     "API REST en Python — utilisé pour P9 Lapage"),
            ("Tableau",     "Visualisation de données — utilisé pour les dashboards P10 et P13"),
            ("Power BI",    "Dashboard métier — utilisé pour le projet P7 Sanitoral"),
            ("DBT",         "Transformation de données en couches — utilisé pour P8"),
            ("Scikit-learn","Librairie de machine learning — utilisé pour P11 et P12"),
        ]

        for tool, desc in outils:
            st.markdown(f"""
            <div style="
                border-left:3px solid #00B4D8;
                padding:0.4rem 0.8rem;
                margin-bottom:0.5rem;
                background:rgba(0,180,216,0.05);
                border-radius: 0 8px 8px 0;
            ">
                <div style="font-weight:600; font-size:0.9rem">{tool}</div>
                <div style="color:#6B7280; font-size:0.8rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("**🧪 Méthodes explorées**")

        methodes = [
            ("Régression logistique, KNN, Random Forest",   "P12 — classification de faux billets"),
            ("Clustering K-Means & CAH",                    "P11 — segmentation et détection"),
            ("Analyse en Composantes Principales (ACP)",    "P11 — réduction dimensionnelle pour clustering pays"),
            ("Pipeline DBT en couches",                     "P8 — staging → intermediate → marts"),
            ("Courbe de Lorenz & coefficient de Gini",      "P9 — analyse de concentration des revenus"),
            ("Tests statistiques Chi-2, ANOVA, Pearson",    "P9 — corrélations et significativité"),
        ]

        for method, desc in methodes:
            st.markdown(f"""
            <div style="
                border-left:3px solid #7C3AED;
                padding:0.4rem 0.8rem;
                margin-bottom:0.5rem;
                background:rgba(124,58,237,0.05);
                border-radius: 0 8px 8px 0;
            ">
                <div style="font-weight:600; font-size:0.9rem">{method}</div>
                <div style="color:#6B7280; font-size:0.8rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# region Tab Profil
with tab1:
    st.subheader("📈 Indicateurs clés")

    kpi_cols = st.columns(4)
    kpis = [
        ("13",  "Projets réalisés",     "P1 → P12 + Stage en entreprise"),
        ("12+", "Outils maîtrisés",     "Python, SQL, Tableau..."),
        ("8",   "Algorithme testés",    "Regression, KNN, Random Forest..."),
        ("4",   "Projets publiés",      "Streamlit"),
    ]

    for col, (value, label, sublabel) in zip(kpi_cols, kpis):
        with col:
            st.markdown(f"""
            <div style="
                background:rgba(0,180,216,0.08);
                border:1px solid #00B4D8;
                border-radius:12px; padding:1rem;
                text-align:center;
            ">
                <div style="font-size:2rem; font-weight:700; color:#00B4D8">{value}</div>
                <div style="font-weight:600; font-size:0.9rem">{label}</div>
                <div style="color:#6B7280; font-size:0.78rem">{sublabel}</div>
            </div>
            """, unsafe_allow_html=True)