import streamlit as st
import pandas as pd
from components.data_loader import get_filtered_df


def make_sidebar(show_categ: bool = True, show_date: bool = True):
    df = st.session_state.df

    with st.sidebar:
        st.header("🎮 Filtres")

        segment_options = sorted(df["segment_client"].dropna().unique().tolist())
        st.pills(
            "Segment client",
            options=segment_options,
            key="selected_segment",
            on_change=lambda: setattr(st.session_state, "selected_segment_value", st.session_state.selected_segment)
        )

        sex_options = sorted(df["sex"].dropna().unique().tolist())
        st.pills(
            "Genre client",
            options=sex_options,
            format_func=lambda x: {'f': 'Femme', 'm': 'Homme'}.get(x, x),
            key="selected_sex",
            on_change=lambda: setattr(st.session_state, "selected_sex_value", st.session_state.selected_sex)
        )

        if show_categ:
            categ_options = ['Tous'] + sorted(df["categ"].dropna().unique().tolist())
            st.pills(
                "Catégorie produit",
                options=categ_options,
                selection_mode='single',
                format_func=lambda x: f"Catégorie {x}" if x in [0, 1, 2] else 'Tous',
                key="selected_categ",
                on_change=lambda: setattr(st.session_state, "selected_categ_value", st.session_state.selected_categ)
            )

        if show_date:
            st.date_input(
                "Période",
                # value=st.session_state.get("date_range_value", (df.date.min(), df.date.max())),
                min_value=df.date.min(),
                max_value=df.date.max(),
                key="date_range",
                on_change=lambda: setattr(st.session_state, "date_range_value", st.session_state.date_range)
            )

        st.button("Réinitialiser", on_click=reset_filters)

def reset_filters():
    df = st.session_state.df
    st.session_state.selected_sex_value = None
    st.session_state.selected_segment_value = None
    st.session_state.selected_categ_value = None
    st.session_state.date_range_value = (df.date.min(), pd.to_datetime(df.date.max()).normalize() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))


def safe_index(options, value):
    try:
        return options.index(value)
    except ValueError:
        return 0  # fallback to first option (None)