import streamlit as st


def render_page(title):
    st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
