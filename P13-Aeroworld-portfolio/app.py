import streamlit as st

st.set_page_config(
    page_title="Portfolio – Patty Chang | Data Analyst",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global CSS
st.markdown("""
<style>
    /* Palette */
    :root {
        --navy:   #1B3A5C;
        --cyan:   #00B4D8;
        --light:  #F0F4F8;
        --white:  #FFFFFF;
        --text:   #1A1A2E;
        --muted:  #6B7280;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--navy);
    }
    [data-testid="stSidebar"] * {
        color: var(--white) !important;
    }
    /* Hide sidebar collapse button */
    [data-testid="stSidebarCollapseButton"] { 
        display: none !important; 
    }

    /* Hide default Streamlit header */
    header[data-testid="stHeader"] { display: none; }

    /* Tag / badge style */
    .tag {
        display: inline-block;
        background-color: #E0F2FE;
        color: #0369A1;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 2px;
    }

    /* Project card */
    .project-card {
        background: var(--white);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s;
    }
    .project-card:hover {
        box-shadow: 0 4px 16px rgba(0,180,216,0.15);
        border-color: var(--cyan);
    }
</style>
""", unsafe_allow_html=True)

# Navigation
pages = {
    "Portfolio": [
        st.Page("pages/1_Accueil.py",            title="Accueil",              icon="🏠"),
        st.Page("pages/2_Profil.py",             title="Mon Profil",           icon="👤"),
        st.Page("pages/3_Projets.py",            title="Projets",              icon="📁"),
        st.Page("pages/4_Tableaux_de_bord.py",   title="Tableaux de bord",     icon="📊"),
        st.Page("pages/5_Gestion_projet.py",     title="Gestion de projet",    icon="🗺️"),
        st.Page("pages/6_Formation_Veille.py",   title="Formation & Veille",   icon="🎓"),
        st.Page("pages/7_Documentation.py",      title="Documentation",        icon="📄"),
    ]
}

nav = st.navigation(pages)
nav.run()