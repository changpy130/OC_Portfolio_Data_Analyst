import streamlit as st
from components.sidebar import render_sidebar
from data.projects import PROJECTS, ALL_TAGS

render_sidebar()

st.title("📁 Projets")
st.caption("Tous les projets réalisés durant la formation Data Analyst — cliquez sur un projet pour voir le détail.")

# region Tag filter

selected_tags = st.multiselect(
    "Filtrer par technologie :",
    options=ALL_TAGS,
    default=[],
    placeholder="Toutes les technologies",
)

st.markdown("---")

# Filter logic
if selected_tags:
    filtered = [
        p for p in PROJECTS
        if any(tag in p.tags for tag in selected_tags)
    ]
else:
    filtered = PROJECTS

# region Project grid

COLS = 2
rows = [filtered[i:i+COLS] for i in range(0, len(filtered), COLS)]

for row in rows:
    cols = st.columns(COLS)
    for col, project in zip(cols, row):
        with col:
            with st.expander(f"{project.icon} {project.id} — {project.title}", expanded=False):

                # Tags
                tags_html = " ".join(
                    f'<span class="tag">{t}</span>' for t in project.tags
                )
                st.markdown(tags_html, unsafe_allow_html=True)
                st.markdown("")

                # Objective
                st.markdown("**🎯 Objectif**")
                st.markdown(project.objective)

                # Skills
                st.markdown("**🛠 Compétences mobilisées**")
                for skill in project.skills:
                    st.markdown(f"- {skill}")

                # Tools
                st.markdown("**💻 Outils**")
                tools_html = " ".join(
                    f'<span class="tag">{t}</span>' for t in project.tools
                )
                st.markdown(tools_html, unsafe_allow_html=True)
                st.markdown("")

                # Insight
                st.markdown("**📈 Insight clé**")
                st.info(project.insight)

                # Soft skills
                st.markdown("**🤝 Soft skills**")
                soft_html = " ".join(
                    f'<span class="tag">{s}</span>' for s in project.soft_skills
                )
                st.markdown(soft_html, unsafe_allow_html=True)
                st.markdown("")

                # Links
                link_cols = st.columns(2)
                with link_cols[0]:
                    if project.repo_url:
                        st.link_button("🐙 Repo GitHub", project.repo_url, width='stretch')
                with link_cols[1]:
                    if project.demo_url:
                        st.link_button("🌐 Live Demo", project.demo_url, width='stretch')