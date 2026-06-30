import streamlit as st
import plotly.graph_objects as go
from components.sidebar import render_sidebar

render_sidebar()

# region Profile

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1B3A5C, #0D2137);
        border-radius: 50%;
        width: 160px; height: 160px;
        display: flex; align-items: center; justify-content: center;
        font-size: 5rem; margin: 1rem auto;
        text-align: center;
    ">👩🏻‍💻</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("## Patty Chang")
    st.markdown("**Data Analyst · Consultante Data**")
    st.markdown("""
        Bilingue anglais–mandarin, niveau B2 en français, je suis une data analyst 
        passionnée par la transformation des données en décisions concrètes. 
        Ancienne développeuse iOS, j'apporte une culture technique solide et 
        une sensibilité produit qui enrichissent ma pratique de la data.
        Je me positionne aujourd'hui comme consultante data, 
        prête à relever les défis analytiques de grandes entreprises comme Aéroworld.
    """)
    st.markdown(
        "🔗 [LinkedIn](https://www.linkedin.com/in/pei-tzu-chang-patty1022/) &nbsp;·&nbsp; "
        "🐙 [GitHub](https://github.com/changpy130)",
        unsafe_allow_html=True
    )

st.markdown("---")

# region radar + soft skills 

left, right = st.columns([3, 2])

with left:
    st.subheader("Compétences techniques")

    skills = {
        "Python":        90,
        "SQL":           75,
        "Power BI":      60,
        "Tableau":       70,
        "DBT":           50,
        "Snowflake":     50,
        "Streamlit":     85,
        "Machine Learning": 55,
        "Statistics":    65,
        "Data Cleaning": 85,
    }

    categories = list(skills.keys())
    values     = list(skills.values())
    # Close the polygon
    categories += [categories[0]]
    values     += [values[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(0, 180, 216, 0.2)",
        line=dict(color="#00B4D8", width=2),
        marker=dict(color="#00B4D8", size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color="#6B7280"),
                gridcolor="#2D3748",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#CBD5E1"),
                gridcolor="#2D3748",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=20, b=20, l=40, r=40),
        height=380,
    )
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader("Soft Skills")

    soft_skills = [
        ("💡", "Curiosité",            "Veille constante, test de nouveaux outils"),
        ("🎨", "Créativité", "Concevoir des visualisations et solutions qui sortent du template"),
        ("🔍", "Esprit analytique",    "Questionner les données avant de conclure"),
        ("⚙️", "Rigueur",              "Documentation, reproductibilité, qualité des livrables"),
        ("📢", "Communication",        "Vulgariser des résultats techniques à tout public"),
    ]

    for icon, title, desc in soft_skills:
        st.markdown(f"""
        <div style="
            border-left: 3px solid #00B4D8;
            padding: 0.5rem 0.8rem;
            margin-bottom: 0.7rem;
            background: rgba(0,180,216,0.05);
            border-radius: 0 8px 8px 0;
        ">
            <div style="font-weight:600;">{title}</div>
            <div style="color:#6B7280; font-size:0.82rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# region Languages

st.subheader("Langues")

lang_cols = st.columns(3)
languages = [
    ("🇬🇧", "Anglais",   "Bilingue",      100),
    ("🇹🇼", "Mandarin",  "Bilingue",      100),
    ("🇫🇷", "Français", "Professionnel (B2)", 72),
]

for col, (flag, lang, level, pct) in zip(lang_cols, languages):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem;
                    border:1px solid #2D3748; border-radius:12px;">
            <div style="font-size:2rem">{flag}</div>
            <div style="font-weight:600; margin:0.3rem 0">{lang}</div>
            <div style="color:#6B7280; font-size:0.85rem; margin-bottom:0.6rem">{level}</div>
            <div style="background:#2D3748; border-radius:999px; height:6px;">
                <div style="background:#00B4D8; width:{pct}%;
                            height:6px; border-radius:999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# region Vision du métier

st.subheader("Ma vision du métier")

v_col1, v_col2 = st.columns(2)

with v_col1:
    st.markdown("**En début de formation**")
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.03);
        border: 1px solid #2D3748;
        border-radius: 12px;
        padding: 1rem;
        color: #9CA3AF;
        font-style: italic;
        line-height: 1.7;
    ">
    Un(e) data analyst me semblait proche du développeur : 
    quelqu'un qui maîtrise des outils techniques pour produire 
    des outputs précis. Venant du développement iOS, je pensais 
    naturellement en termes de code, de structure et de livraison.
    </div>
    """, unsafe_allow_html=True)

with v_col2:
    st.markdown("**Aujourd'hui**")
    st.markdown("""
    <div style="
        background: rgba(0,180,216,0.07);
        border: 1px solid #00B4D8;
        border-radius: 12px;
        padding: 1rem;
        line-height: 1.7;
    ">
    Un(e) data analyst est avant tout un <strong>traducteur</strong> entre 
    les données et les décisions métier. La vraie valeur est dans la 
    capacité à comprendre un besoin, challenger les hypothèses, 
    communiquer clairement et choisir le bon outil pour le bon problème.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# region Axes d'amélioration

st.subheader("Axes d'amélioration")

axes = st.columns(3)
ameliorations = [
    ("🤖", "Machine Learning",  "Approfondir Scikit-learn et les modèles prédictifs au-delà de l'EDA"),
    ("☁️", "Cloud & DataOps",   "Renforcer les compétences Azure / GCP et les pipelines de données en production"),
    ("📱", "Transition dev → data", "Capitaliser sur mon expérience iOS pour aborder les sujets DataOps avec une culture engineering solide"),
]

for col, (icon, title, desc) in zip(axes, ameliorations):
    with col:
        st.markdown(f"""
        <div style="
            border:1px solid #2D3748; border-radius:12px;
            padding:1rem; text-align:center;
        ">
            <div style="font-size:1.8rem">{icon}</div>
            <div style="font-weight:600; margin:0.4rem 0">{title}</div>
            <div style="color:#6B7280; font-size:0.83rem">{desc}</div>
        </div>
        """, unsafe_allow_html=True)