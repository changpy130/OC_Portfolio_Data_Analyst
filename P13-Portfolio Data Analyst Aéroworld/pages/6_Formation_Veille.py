import streamlit as st
from components.sidebar import render_sidebar
from components.helper import show_pdf

render_sidebar()

st.title("🎓 Formation & Veille")
st.caption("Vidéo de formation sur Tableau et veille technologique continue.")

tab1, tab2 = st.tabs(["Vidéo de formation", "Veille technologique"])

# region TAB 1 VIDEO

with tab1:

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Vidéo de formation : Créer une visualisation avec Tableau")
        st.markdown("""
        Cette vidéo de formation explique pas à pas comment créer une visualisation 
        de données avec **Tableau Software**, depuis la connexion à une source de données 
        jusqu'à la publication d'un dashboard interactif.
        """)

    with col2:
        st.markdown(f"""
        <div style="
            background:rgba(0,180,216,0.08);
            border:1px solid #00B4D8;
            border-radius:12px; padding:1rem;
            text-align:center;
            margin-bottom: 32px;
        ">
            <div style="font-size:1.8rem">⏱️</div>
            <div style="font-weight:700; font-size:1.4rem; color:#00B4D8">8 min+</div>
            <div style="color:#6B7280; font-size:0.82rem">Durée minimale requise</div>
        </div>
        """, unsafe_allow_html=True)

    # Video embed
    VIDEO_URL = "https://youtu.be/oJ9-8M0PyA8"

    st.video(VIDEO_URL)
    st.caption("Voix générée par logiciel de synthèse vocale pour préserver la confidentialité")
    
    st.markdown("---")

    # What you'll learn
    st.subheader("Ce que vous apprendrez")

    learn_cols = st.columns(3)
    learnings = [
        ("🔌", "Connexion aux données",
               "Connecter Tableau à différentes sources : CSV, Excel, base de données"),
        ("📊", "Choix du bon graphique",
               "Identifier le type de visualisation adapté à vos données et votre message"),
        ("🎨", "Mise en forme",
               "Personnaliser couleurs, polices, tooltips et légendes pour un rendu professionnel"),
        ("🔍", "Filtres & interactions",
               "Ajouter des filtres dynamiques et des actions pour rendre le dashboard interactif"),
        ("📖", "Storytelling",
               "Construire une histoire cohérente avec vos données pour convaincre votre audience"),
        ("🌐", "Publication",
               "Publier votre dashboard sur Tableau Public et partager le lien"),
    ]

    for i, (icon, title, desc) in enumerate(learnings):
        with learn_cols[i % 3]:
            st.markdown(f"""
            <div style="
                border:1px solid #2D3748; border-radius:12px;
                padding:1rem; margin-bottom:1rem; text-align:center;
            ">
                <div style="font-size:1.8rem">{icon}</div>
                <div style="font-weight:600; margin:0.4rem 0; font-size:0.9rem">{title}</div>
                <div style="color:#6B7280; font-size:0.8rem; line-height:1.5">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Public cible
    st.subheader("🎯 Public cible")
    st.markdown("""
    <div style="
        background:rgba(0,180,216,0.05);
        border:1px solid #2D3748;
        border-radius:12px; padding:1.2rem;
        line-height:1.8;
    ">
        Cette formation s'adresse aux <strong>utilisateurs débutants ou intermédiaires</strong> 
        souhaitant créer leurs premières visualisations de données avec Tableau Software.
    </div>
    """, unsafe_allow_html=True)

# region TAB 2 VEILLE

with tab2:
    # Tendances
    st.subheader("📈 Tendances suivies")

    tendances = [
        ("🤖", "IA générative & data",
               "L'intégration de LLMs dans les workflows data (copilots SQL, génération de dashboards) "
               "transforme le métier. Le data analyst doit savoir prompter et critiquer les outputs IA."),
        ("☁️", "Cloud & DataOps",
               "La montée en puissance des plateformes cloud (Snowflake, BigQuery, Databricks) "
               "et des pratiques DataOps (tests, CI/CD data, documentation) devient incontournable."),
        ("🔒", "Data governance & RGPD",
               "La qualité, la traçabilité et la sécurité des données deviennent des priorités "
               "dans les grandes entreprises comme Aéroworld."),
    ]

    for icon, title, desc in tendances:
        st.markdown(f"""
        <div style="
            border-left:3px solid #00B4D8;
            border-right:3px solid #00B4D8;
            padding:0.8rem 1rem;
            margin-bottom:0.8rem;
            background:rgba(0,180,216,0.05);
            border-radius: 8px;
        ">
            <div style="font-weight:600; font-size:0.95rem">{title}</div>
            <div style="color:#9CA3AF; font-size:0.85rem; margin-top:0.3rem; line-height:1.6">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Outils testés
    st.subheader("🛠️ Outils testés & comparés")

    outils_data = [
        ("Streamlit",  "Power BI",   "Dashboard interactif",
         "Streamlit offre plus de flexibilité pour les développeurs ; "
         "Power BI est plus accessible aux équipes métier non-techniques."),
        ("Tableau",    "Power BI",   "Visualisation de données",
         "Tableau excelle en exploration visuelle et storytelling ; "
         "Power BI s'intègre mieux dans l'écosystème Microsoft."),
        ("DBT",        "Pandas",     "Transformation de données",
         "DBT apporte tests, documentation et versioning natifs ; "
         "Pandas reste plus flexible pour l'exploration ad hoc."),
    ]

    for tool1, tool2, use_case, comparison in outils_data:
        with st.expander(f"{tool1} vs {tool2} : {use_case}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style="
                    background:rgba(0,180,216,0.08);
                    border:1px solid #00B4D8;
                    border-radius:10px; padding:0.8rem;
                    text-align:center;
                ">
                    <div style="font-weight:700; color:#00B4D8">{tool1}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="
                    background:rgba(124,58,237,0.08);
                    border:1px solid #7C3AED;
                    border-radius:10px; padding:0.8rem;
                    text-align:center;
                ">
                    <div style="font-weight:700; color:#7C3AED">{tool2}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="
                margin-top:0.8rem; padding:0.8rem;
                background:rgba(255,255,255,0.03);
                border-radius:8px; color:#9CA3AF;
                font-size:0.88rem; line-height:1.6;
            ">
                {comparison}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Sources
    st.subheader("📚 Sources & ressources")

    sources = [
        ("📰", "Towards Data Science",     "https://towardsdatascience.com",
               "Articles techniques Python, ML, visualisation"),
        ("📊", "Tableau Blog",             "https://www.tableau.com/blog",
               "Bonnes pratiques et nouveautés Tableau"),
        ("🐍", "Real Python",             "https://realpython.com",
               "Tutoriels Python approfondis"),
        ("🔧", "DBT Documentation",        "https://docs.getdbt.com",
               "Référence officielle DBT"),
        ("🤗", "Hugging Face Blog",        "https://huggingface.co/blog",
               "Actualités IA et LLMs"),
        ("🇫🇷", "Le Wagon Blog",           "https://www.lewagon.com/blog",
               "Data science en français"),
    ]

    src_cols = st.columns(3)
    for i, (icon, name, url, desc) in enumerate(sources):
        with src_cols[i % 3]:
            st.markdown(f"""
            <div style="
                border:1px solid #2D3748; border-radius:12px;
                padding:0.8rem; margin-bottom:0.8rem;
            ">
                <div style="font-size:1.3rem">{icon}</div>
                <div style="font-weight:600; font-size:0.88rem; margin:0.3rem 0">
                    <a href="{url}" target="_blank" 
                       style="color:#00B4D8; text-decoration:none;">{name}</a>
                </div>
                <div style="color:#6B7280; font-size:0.78rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)