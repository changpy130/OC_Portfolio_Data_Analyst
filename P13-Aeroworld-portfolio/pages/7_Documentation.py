import streamlit as st
from components.sidebar import render_sidebar
from components.helper import show_pdf_download
import os
from pathlib import Path

render_sidebar()

st.title("📄 Documentation")
st.caption("Procédures, posture consultant et informations sur ce portfolio.")

tab1, tab2, tab3 = st.tabs([
    "Procédure graphique",
    "Posture consultant",
    "À propos"
])

# region TAB 1 PROCEDURE

BASE_DIR = Path(__file__).parent.parent
PDF_PATH = BASE_DIR / "assets" / "procedure_graphique.pdf"
PDF_ORIGINAL_PATH = BASE_DIR / "assets" / "procedure_graphique_original.pdf"

with tab1:
    st.subheader("Procédure de création d'un graphique data")
    st.markdown("""
    Guide pas à pas pour créer une visualisation de données claire et professionnelle 
    avec Tableau Software, depuis la préparation des données jusqu'à la publication.
    """)

    # PDF embed
    show_pdf_download(PDF_ORIGINAL_PATH, "procedure_graphique")

    st.markdown("---")

    # Steps preview
    st.subheader("Aperçu des étapes")
    st.caption("Résumé de la procédure")

    steps = [
        ("1", "Préparer les données",
              "Nettoyer et structurer vos données dans un format tabulaire (CSV, Excel). "
              "Vérifier les types, les valeurs manquantes et les doublons avant d'importer."),
        ("2", "Connecter à Tableau",
              "Ouvrir Tableau Desktop ou Tableau Public. "
              "Connecter votre source de données via Fichier → Ouvrir ou Données → Nouvelle source."),
        ("3", "Choisir le bon graphique",
              "Identifier le message à communiquer : comparaison → barres, "
              "évolution → ligne, répartition → camembert, corrélation → nuage de points."),
        ("4", "Construire la visualisation",
              "Glisser les dimensions sur les lignes/colonnes, les mesures sur les étagères. "
              "Tableau génère automatiquement une visualisation de base."),
        ("5", "Mettre en forme",
              "Personnaliser couleurs, polices, titres, tooltips et légendes. "
              "Appliquer une palette cohérente et accessibles aux daltoniens."),
        ("6", "Ajouter des filtres & interactions",
              "Créer des filtres dynamiques, des actions entre feuilles "
              "et des paramètres pour rendre le dashboard interactif."),
        ("7", "Vérifier & tester",
              "Tester le dashboard avec des utilisateurs cibles. "
              "Vérifier la lisibilité sur différentes tailles d'écran."),
        ("8", "Publier",
              "Publier sur Tableau Public via Serveur → Publier sur Tableau Public. "
              "Copier le lien d'intégration pour partager ou embarquer dans un portfolio."),
    ]

    for step_num, title, desc in steps:
        st.markdown(f"""
        <div style="
            display:flex; gap:1rem; align-items:flex-start;
            margin-bottom:0.8rem;
            padding:0.8rem;
            border:1px solid #2D3748;
            border-radius:12px;
        ">
            <div style="
                background:#00B4D8; color:white;
                border-radius:50%; width:32px; height:32px;
                display:flex; align-items:center; justify-content:center;
                font-weight:700; font-size:0.9rem; flex-shrink:0;
            ">{step_num}</div>
            <div>
                <div style="font-weight:600; margin-bottom:0.2rem">{title}</div>
                <div style="color:#9CA3AF; font-size:0.85rem; line-height:1.6">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# region TAB 2 POSTURE

with tab2:
    # 4 pillars
    st.subheader("Les 4 piliers de la posture consultant")

    pillars = [
        ("🔍", "Challenger les besoins",
               "Ne pas exécuter une demande sans la questionner.",
               [
                   "Pourquoi avez-vous besoin de ce graphique ?",
                   "Est-ce que ce KPI mesure vraiment ce que vous voulez savoir ?",
                   "Un tableau de bord est-il la meilleure solution ici ?",
               ]),
        ("📢", "Communiquer avec tout public",
               "Adapter son discours selon l'interlocuteur.",
               [
                   "Avec un ingénieur : parler technique, montrer le code",
                   "Avec un directeur : parler impact business, pas de jargon",
                   "Avec un utilisateur : être pédagogue, montrer pas à pas",
               ]),
        ("🎓", "Former et accompagner",
               "Partager la connaissance.",
               [
                   "Créer des guides et procédures clairs",
                   "Former les équipes à la prise en main",
                   "Être disponible pour les questions post-livraison",
               ]),
        ("⚙️", "Rigueur & traçabilité",
               "Documenter pour garantir la reproductibilité.",
               [
                   "Versionner le code (GitHub)",
                   "Documenter les choix méthodologiques",
                   "Assurer la conformité RGPD",
               ]),
    ]

    for icon, title, subtitle, examples in pillars:
        with st.expander(f"{title}", expanded=False):
            st.markdown(f"*{subtitle}*")
            st.markdown("**Exemples concrets :**")
            for ex in examples:
                st.markdown(f"→ {ex}")

    st.markdown("---")

    # Exemples dans les projets
    st.subheader("Cette posture dans mes projets")

    exemples = [
        ("P10 DWFA",
         "Posture consultant",
         "Plutôt que de simplement produire des graphiques, j'ai challengé le besoin "
         "de l'ONG en proposant trois angles d'analyse distincts (création, modernisation, "
         "consulting gouvernemental)."),
        ("P7 Sanitoral",
         "Communication multi-profils",
         "Conception d'un dashboard à trois niveaux (directeur général, régional, pays) "
         "avec un discours visuel adapté à chaque audience."),
        ("P9 Lapage",
         "Rigueur & traçabilité",
         "Mise en place d'un pipeline CI/CD complet avec tests automatisés (pytest) "
         "et GitHub Actions; chaque modification est vérifiée avant déploiement."),
        ("P13 Portfolio",
         "Former & accompagner",
         "Création d'une vidéo de formation Loom et d'une procédure documentée "
         "pour accompagner les utilisateurs dans la prise en main de Tableau."),
    ]

    for project, competence, desc in exemples:
        st.markdown(f"""
        <div style="
            border-left:3px solid #00B4D8;
            padding:0.8rem 1rem;
            margin-bottom:0.8rem;
            background:rgba(0,180,216,0.05);
            border-radius: 8px;
        ">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:600">{project}</div>
                <span style="
                    background:#1B3A5C; color:#00B4D8;
                    padding:2px 10px; border-radius:999px;
                    font-size:0.78rem;
                ">{competence}</span>
            </div>
            <div style="color:#9CA3AF; font-size:0.85rem; margin-top:0.4rem; line-height:1.6">
                {desc}
            </div>
        </div>
        """, unsafe_allow_html=True)

# region TAB 3 A PROPOS

with tab3:
    st.subheader("À propos de ce portfolio")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Comment ce portfolio a été construit**")
        st.markdown("""
        <div style="
            border:1px solid #2D3748; border-radius:12px;
            padding:1rem; line-height:1.9;
        ">
            <div><strong>Framework :</strong> Streamlit (Python)</div>
            <div><strong>Design :</strong> CSS custom, palette aéronautique</div>
            <div><strong>Dashboards :</strong> Tableau Public</div>
            <div><strong>Documents :</strong> Canva → PDF</div>
            <div><strong>Déploiement :</strong> Streamlit Community Cloud</div>
            <div><strong>Versioning :</strong> GitHub</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("**Conformité RGPD**")
        st.markdown("""
        <div style="
            border:1px solid #2D3748; border-radius:12px;
            padding:1rem; line-height:1.9;
        ">
            <div>Aucune donnée personnelle des visiteurs collectée</div>
            <div>Hébergé sur plateforme publique (Streamlit Cloud)</div>
            <div>Informations publiées volontairement par la candidate</div>
            <div>Suppression possible à tout moment</div>
            <div>Pas de cookies tiers ou trackers analytiques</div>
            <div>Une voix synthétisée pour préserver la confidentialité</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Contact")

    contact_cols = st.columns(2)

    with contact_cols[0]:
        st.link_button(
            "🔗 LinkedIn",
            "https://www.linkedin.com/in/pei-tzu-chang-patty1022/",
            width='stretch'
        )
    with contact_cols[1]:
        st.link_button(
            "🐙 GitHub",
            "https://github.com/changpy130",
            width='stretch'
        )

st.caption("Dernière mise à jour : Juin 2026")