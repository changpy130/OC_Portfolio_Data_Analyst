import streamlit as st
from components.sidebar import render_sidebar
from data.projects import PROJECTS, ALL_TOOLS

render_sidebar()

st.markdown("""
<div style="
    background: linear-gradient(135deg, #1B3A5C 0%, #0D2137 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem;
    color: white;
    margin-bottom: 2rem;
">
    <h1 style="color:white; margin:0; font-size:2.4rem;">
        Bonjour, je suis Patty Chang ✨
    </h1>
    <p style="color:#00B4D8; font-size:1.15rem; margin:0.5rem 0 1.5rem 0;">
        Data Analyst · Consultante Data
    </p>
    <p style="color:#CBD5E1; max-width:620px; line-height:1.7;">
        Ce portfolio présente mon parcours, mes projets et les livrables 
        réalisés dans le cadre du projet P13 d'OpenClassrooms en réponse à la demande de recrutement d'<strong style="color:white;">Aéroworld</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# region Compétences Aéroworld
st.subheader("Ce que ce portfolio démontre")

competences = [
    ("🔍", "Analyse du besoin métier",    "Identifier les enjeux et contraintes client"),
    ("📋", "Cahier des charges",          "Formaliser les besoins et les solutions"),
    ("🗂️", "Gestion de projet",           "Organiser avec Gantt et outils projet"),
    ("📊", "Visualisation de données",    "Tableaux de bord Power BI & Tableau"),
    ("🎓", "Formation & accompagnement",  "Vidéo de formation, prise en main des outils"),
    ("📄", "Documentation",              "Procédures claires et reproductibles"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(competences):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="
            border:1px solid #E2E8F0; border-radius:12px;
            padding:1rem; margin-bottom:1rem; text-align:center;
        ">
            <div style="font-size:1.8rem">{icon}</div>
            <div style="font-weight:600; margin:0.4rem 0">{title}</div>
            <div style="color:#6B7280; font-size:0.85rem">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# region Projets résumé
st.subheader(f"Projets réalisés ({len(PROJECTS)})")

cols2 = st.columns(4)
for i, p in enumerate(PROJECTS):
    with cols2[i % 4]:
        st.markdown(f"""
        <div style="
            border:1px solid #E2E8F0;
            border-radius:10px; padding-bottom:32px; padding-top:32px;
            margin-bottom:2rem; text-align:center;
        ">
            <div style="font-weight:600; font-size:1.2rem">{p.id}</div>
            <div style="font-size:0.8rem; line-height:1.4;">{p.title}</div>
        </div>
        """, unsafe_allow_html=True)

# region Tech badges
st.subheader("Compétences techniques")

all_tools = [
    "Python", "SQL", "Scikit-learn", 
    "Streamlit", "FastAPI", "GitHub Actions",
    "Power BI", "Tableau", "DBT", "Snowflake",
    "Plotly"
]

badges = " ".join(
    f'<span class="tag">{t}</span>' for t in all_tools
)
st.markdown(badges, unsafe_allow_html=True)