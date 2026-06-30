import base64
import streamlit as st

def show_pdf(filepath, height=700, toolbar=True):
    with open(filepath, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    
    if toolbar:
        st.markdown(f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" 
                height="{height}px"
                style="border:none; border-radius:12px;">
            </iframe>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}#toolbar=0" 
                width="100%" 
                height="{height}px"
                style="border:none; border-radius:12px;">
            </iframe>
        """, unsafe_allow_html=True)

def show_pdf_download(path, name):
    with open(str(path), "rb") as f:
        st.download_button(
            label="📥 Télécharger le fichier complet en PDF",
            data=f,
            file_name=f"{name}.pdf",
            mime="application/pdf",
        )