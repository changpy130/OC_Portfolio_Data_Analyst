import streamlit as st
from components.data_loader import load_data

# init session_state
def init_state():
    init_df()
    init_defaults()

    
def init_defaults():
    if "selected_sex_value" not in st.session_state:
        st.session_state.selected_sex_value = None
    if "selected_segment_value" not in st.session_state:
        st.session_state.selected_segment_value = None
    if "selected_categ_value" not in st.session_state:
        st.session_state.selected_categ_value = None
    if "date_range_value" not in st.session_state:
        df = st.session_state.df
        st.session_state.date_range_value = (df.date.min(), df.date.max())

    # Always sync widget keys from _value keys before render
    st.session_state.selected_segment = st.session_state.selected_segment_value
    st.session_state.selected_sex = st.session_state.selected_sex_value
    st.session_state.selected_categ = st.session_state.selected_categ_value
    st.session_state.date_range = st.session_state.date_range_value


def init_df():
    if "df" not in st.session_state:
        st.session_state.df = load_data()