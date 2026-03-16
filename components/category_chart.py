"""Top Categorias - Barras horizontais com Plotly."""
#components/category_chart.py


import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.revenue_chart import get_base_layout


CATEGORY_COLORS = [
    "#2DD4A8", "#F5A623", "#38BDF8", "#F43F5E", "#A78BFA",
    "#2DD4A8", "#F5A623", "#38BDF8", "#F43F5E", "#A78BFA",
]


def render_category_chart(category_df: pd.DataFrame, key: str):
    """Renderiza grafico de barras horizontais das top categorias."""

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Top Categorias</div>
        <div class="section-subtitle">Categorias com maior receita</div>
    </div>
    """, unsafe_allow_html=True)

    top8 = category_df.head(8).iloc[::-1]  # Reverso para plotar de cima pra baixo

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top8["revenue"],
        y=top8["category"],
        orientation="h",
        marker=dict(
            color=CATEGORY_COLORS[:len(top8)][::-1],
            cornerradius=6,
        ),
        hovertemplate="<b>%{y}</b><br>Receita: R$ %{x:,.2f}<br><extra></extra>",
        opacity=0.9,
    ))

    layout = get_base_layout()
    layout["margin"]["l"] = 10
    layout["xaxis"]["tickprefix"] = "R$ "
    layout["height"] = 350
    fig.update_layout(**layout)

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
        key=key
    )
