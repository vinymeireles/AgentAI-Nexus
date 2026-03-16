"""Metodos de Pagamento - Donut chart com Plotly."""
#components/payment_chart.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.revenue_chart import get_base_layout


DONUT_COLORS = ["#2DD4A8", "#F5A623", "#38BDF8", "#F43F5E", "#A78BFA"]


def render_payment_chart(payment_df: pd.DataFrame, key: str):
    """Renderiza grafico donut de metodos de pagamento."""

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Metodos de Pagamento</div>
        <div class="section-subtitle">Distribuicao por forma de pagamento</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=payment_df["label"],
        values=payment_df["count"],
        hole=0.55,
        marker=dict(
            colors=DONUT_COLORS[:len(payment_df)],
            line=dict(color="#0d1117", width=2),
        ),
        textinfo="percent",
        textfont=dict(size=11, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
    ))

    layout = get_base_layout()
    layout["height"] = 350
    layout["annotations"] = [dict(
        text="Pagamentos",
        x=0.5, y=0.5,
        font=dict(size=13, color="#8b9dc3", family="Space Grotesk, sans-serif"),
        showarrow=False,
    )]

    fig.update_layout(**layout)

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
        key=key
    )
