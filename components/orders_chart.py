"""Grafico de Pedidos por Mes - Bar chart com Plotly."""
#components/orders_chart.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.revenue_chart import get_base_layout


def render_orders_chart(monthly_df: pd.DataFrame):
    """Renderiza grafico de barras de pedidos por mes."""

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Pedidos por Mes</div>
        <div class="section-subtitle">Volume de pedidos ao longo de 2024</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly_df["month"],
        y=monthly_df["orders"],
        marker=dict(
            color="#F5A623",
            cornerradius=6,
        ),
        hovertemplate="<b>%{x}</b><br>Pedidos: %{y}<extra></extra>",
        opacity=0.9,
    ))

    layout = get_base_layout()
    layout["xaxis"]["showgrid"] = False
    fig.update_layout(**layout)

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
