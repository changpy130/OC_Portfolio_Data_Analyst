import streamlit as st
import pandas as pd

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import load_all_clients, get_basic_kpis


@st.cache_data
def load_data():
    df = load_all_clients()
    df["date"] = pd.to_datetime(df["date"])
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 25, 35, 50, 100],
        labels=["<25", "25-35", "35-50", "50+"]
    )
    return df


def get_filtered_df() -> pd.DataFrame:
    df = st.session_state.df.copy()
    
    if st.session_state.get("selected_sex_value") not in (None, "Tous"):
        df = df.loc[df.sex == st.session_state.selected_sex_value]

    if st.session_state.get("selected_segment_value") not in (None, "Tous"):
        df = df.loc[df.segment_client == st.session_state.selected_segment_value]
    
    if st.session_state.get("selected_categ_value") not in (None, "Tous"):
        df = df.loc[df.categ == st.session_state.selected_categ_value]

    if st.session_state.get("date_range_value"):
        date_range = st.session_state.date_range_value
        end = pd.to_datetime(st.session_state.df.date.max()).normalize() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        
        # only start date chosen so far
        if len(date_range) == 1:
            start = pd.to_datetime(date_range[0])
            end = end
        else:
            start, end = date_range
            start = pd.to_datetime(start)
            end = pd.to_datetime(end).normalize() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        df = df[(df["date"] >= start) & (df["date"] <= end)]

    return df