import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from components.sidebar import render_sidebar
from components.helper import show_pdf, show_pdf_download
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
ANALYSE_BESOIN_PATH = BASE_DIR / "assets" / "analyse_besoin.pdf"
CAHIER_PATH = BASE_DIR / "assets" / "cahier_des_charges.pdf"
CARTE_MENTALE_PATH = BASE_DIR / "assets" / "carte_mentale.pdf"
MOCKUP_VEILLE_PATH = BASE_DIR / "assets" / "mockup_veille.png"

render_sidebar()

st.title("🗺️ Gestion de projet Portfolio")
st.caption("Le portfolio P13 géré comme un vrai projet data : analyse du besoin, cadrage, planification.")

st.markdown("---")

# region Analyse du besoin métier

st.subheader("🔍 Analyse du besoin métier client")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Le client : Aéroworld**")
    st.markdown("""
    <div style="
        border:1px solid #2D3748; border-radius:12px;
        padding:1rem; line-height:1.8;  margin-bottom:1rem;
    ">
        <div>🏭  <strong>Secteur :</strong> Industrie aéronautique internationale</div>
        <div>👥  <strong>Taille :</strong> Plusieurs milliers d'employés, présence mondiale</div>
        <div>📊  <strong>Besoin data :</strong> Gestion de données massives multi-sources</div>
        <div>🎯  <strong>Recrutement :</strong> Chef de projet en analyse data</div>
        <div>🌍  <strong>Atout :</strong> Anglais technique apprécié</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("**Problématique data identifiée**")
    st.markdown("""
    <div style="
        border:1px solid #2D3748; border-radius:12px;
        padding:1rem; line-height:1.8; margin-bottom:1rem;
    ">
        <div>⚠️ Volume massif de données (essais en vol, capteurs, maintenance)</div>
        <div style="margin-top:0.5rem">⚠️ Intégration et interopérabilité de sources hétérogènes</div>
        <div style="margin-top:0.5rem">⚠️ Sécurité et confidentialité</div>
        <div style="margin-top:0.5rem">⚠️ Besoin d'infrastructures robustes (ML, IA)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Compétences attendues par Aéroworld**")

competences = [
    ("🔍", "Veille métier & technologique",     "Tester de nouveaux outils, techniques et méthodes"),
    ("🎯", "Identification des besoins métier",  "Intégrer les contraintes pour définir objectifs et enjeux"),
    ("📋", "Cahier des charges fonctionnel",     "Cadrer les besoins et les solutions"),
    ("🗂️", "Organisation de projet data",        "Utiliser des outils de gestion de projet"),
    ("🎓", "Accompagnement des équipes",         "Formation à la prise en main des outils"),
    ("📄", "Procédures de documentation",        "Assurer une gestion fiable et reproductible"),
]

cols = st.columns(2)
for i, (icon, title, desc) in enumerate(competences):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="
            border-right:3px solid #00B4D8;
            border-left:3px solid #00B4D8;
            padding:0.5rem 0.8rem;
            margin-bottom:1rem;
            background:rgba(0,180,216,0.05);
            border-radius: 8px;
        ">
            <div style="font-weight:600;">{icon}  {title}</div>
            <div style="color:#6B7280; font-size:0.82rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

show_pdf_download(ANALYSE_BESOIN_PATH, "analyse_besoin")

st.markdown("---")

# region Cahier des charges 

st.subheader("📋 Cahier des charges du projet portfolio")

cdc_cols = st.columns(3)

with cdc_cols[0]:
    st.markdown("""
    <div style="border:1px solid #2D3748; border-radius:12px; padding:1rem; margin-bottom:1rem;">
        <div style="font-weight:600; margin-bottom:1rem;">🎯 Objectif</div>
        <div style="color:#9CA3AF; font-size:0.88rem; line-height:1.6;">
            Constituer un portfolio réflexif et visuel démontrant la maîtrise 
            des compétences attendues par Aéroworld pour un poste de 
            chef de projet en analyse data.
        </div>
    </div>
    """, unsafe_allow_html=True)

with cdc_cols[1]:
    st.markdown("""
    <div style="border:1px solid #2D3748; border-radius:12px; padding:1rem;">
        <div style="font-weight:600; margin-bottom:1rem;">📦 Livrables attendus</div>
        <div style="color:#9CA3AF; font-size:0.88rem; line-height:1.6;">
            Carte mentale · Analyse du besoin · Cahier des charges · 
            Diagramme de Gantt · Mock-ups · Tableaux de bord · 
            Vidéo de formation · Documentation · Portfolio en ligne
        </div>
    </div>
    """, unsafe_allow_html=True)

with cdc_cols[2]:
    st.markdown("""
    <div style="border:1px solid #2D3748; border-radius:12px; padding:1rem;">
        <div style="font-weight:600; margin-bottom:1rem;">⚙️ Contraintes</div>
        <div style="color:#9CA3AF; font-size:0.88rem; line-height:1.6;">
            Format : CMS ou page GitHub · Présentation orale en soutenance · 
            Posture consultant obligatoire · Livrables validés par étapes 
            avec le mentor
        </div>
    </div>
    """, unsafe_allow_html=True)

show_pdf_download(CAHIER_PATH, "cahier_des_charges")

st.markdown("---")

# region Gantt 

st.subheader("📅 Diagramme de Gantt")

tasks = [
    # (Étape, Task label, Start, End, Status)
    ("Étape 1", "Carte mentale",                    "2026-06-01", "2026-06-05", "Terminé"),
    ("Étape 2", "Analyse du besoin métier",         "2026-06-05", "2026-06-08", "Terminé"),
    ("Étape 2", "Cahier des charges portfolio",     "2026-06-08", "2026-06-11", "Terminé"),
    ("Étape 2", "Diagramme de Gantt",               "2026-06-09", "2026-06-10", "Terminé"),
    ("Étape 3", "Mock-up tableau de bord Veille",   "2026-06-10", "2026-06-11", "Terminé"),
    ("Étape 3", "Mock-up tableau de bord Profil",   "2026-06-11", "2026-06-12", "Terminé"),
    ("Étape 3", "Mock-up portfolio",                "2026-06-12", "2026-06-14", "Terminé"),
    ("Étape 4", "Tableau de bord Veille (Power BI/Tableau)", "2026-06-19", "2026-06-24", "Terminé"),
    ("Étape 4", "Tableau de bord Profil (Power BI/Tableau)", "2026-06-19", "2026-06-24", "Terminé"),
    ("Étape 4", "Vidéo de formation (Loom)",        "2026-06-25", "2026-06-30", "Terminé"),
    ("Étape 4", "Documentation & procédures",       "2026-06-27", "2026-07-01", "Terminé"),
    ("Étape 5", "Construction portfolio Streamlit", "2026-06-14", "2026-07-01", "Terminé"),
    ("Étape 5", "Soutenance blanche (mentor)",      "2026-07-01", "2026-07-05", "Terminé"),
    ("Étape 5", "Soutenance finale Aéroworld",      "2026-07-05", "2026-07-10", "À venir"),
]

# Color per status
color_map = {
    "Terminé":  "#0C5D37",
    "En cours": "#F59E0B",
    "À venir":  "#6B7280",
}

# to have Step 1 on the top
tasks.reverse()

fig = go.Figure()

seen_statuses = set()

for i, (etape, task, start, end, status) in enumerate(tasks):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt   = datetime.strptime(end,   "%Y-%m-%d")
    label    = f"{etape} · {task}"
    show_leg = status not in seen_statuses
    seen_statuses.add(status)

    fig.add_trace(go.Scatter(
        x=[start_dt, end_dt],
        y=[label, label],
        mode="lines",
        line=dict(color=color_map[status], width=18),
        name=status,
        showlegend=show_leg,
        hovertemplate=(
            f"{etape}<br>"
            f"<b>{task}</b><br>"
            f"Début : {start}<br>"
            f"Fin : {end}<br>"
            f"Statut : {status}<extra></extra>"
        ),
    ))

fig.add_vline(
    x=datetime.now(),
    line_dash="dash",
    line_color="#EF4444",
    annotation_text="Aujourd'hui",
    annotation_font_color="#EF4444",
    annotation_position="top",
)

fig.update_layout(
    barmode="overlay",
    xaxis=dict(
        tickformat="%b %Y",
        gridcolor="#2D3748",
        tickfont=dict(color="#9CA3AF"),
    ),
    yaxis=dict(
        tickfont=dict(color="#CBD5E1", size=12),
        gridcolor="#2D3748",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=520,
    margin=dict(l=10, r=20, t=20, b=20),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right",  x=1,
        font=dict(color="#CBD5E1"),
    ),
)

st.plotly_chart(fig, width='stretch')
st.markdown("---")

# region Carte mentale

st.subheader("🧠 Carte mentale")
st.caption("Vue d'ensemble du portfolio : organisation des idées et liens entre les livrables.")
show_pdf_download(CARTE_MENTALE_PATH, "carte_mentale")

st.markdown("---")

# region Mock-ups

st.subheader("🖼️ Mock-ups")
st.caption("Maquettes réalisées avant la construction des tableaux de bord et du portfolio.")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("**Dashboard Veille**")
    st.image(str(MOCKUP_VEILLE_PATH), width='stretch')

with m2:
    st.markdown("**Dashboard Profil**")
    st.image("assets/mockup_profil.png", width='stretch')

with m3:
    st.markdown("**Portfolio**")
    st.image("assets/mockup_portfolio.png", width='stretch')