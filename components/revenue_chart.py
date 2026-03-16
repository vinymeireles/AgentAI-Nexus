"""Grafico de Receita Mensal - Area chart com Plotly."""

# components/revenue_chart.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd


CHART_COLORS = {
    "emerald": "#2DD4A8",
    "emerald_light": "rgba(45, 212, 168, 0.15)",
    "grid": "#1e2a3a",
    "text": "#8b9dc3",
    "bg": "rgba(0,0,0,0)",
}


def get_base_layout(title: str = "") -> dict:
    return dict(
        paper_bgcolor=CHART_COLORS["bg"],
        plot_bgcolor=CHART_COLORS["bg"],
        font=dict(family="Inter, sans-serif", color=CHART_COLORS["text"], size=12),
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(
            gridcolor=CHART_COLORS["grid"],
            showgrid=False,
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=CHART_COLORS["grid"],
            showgrid=True,
            gridwidth=1,
            tickfont=dict(size=11),
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#1c2333",
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor="#2a3346",
        ),
        height=320,
    )


def render_revenue_chart(monthly_df: pd.DataFrame, key: str):
    st.markdown("""
    <div class="section-card">
        <div class="section-title">Receita Mensal</div>
        <div class="section-subtitle">Evolucao da receita ao longo de 2024</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df["month"],
        y=monthly_df["revenue"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor=CHART_COLORS["emerald_light"],
        line=dict(color=CHART_COLORS["emerald"], width=2.5, shape="spline"),
        marker=dict(size=6, color=CHART_COLORS["emerald"]),
        hovertemplate="<b>%{x}</b><br>Receita: R$ %{y:,.2f}<extra></extra>",
    ))

    layout = get_base_layout()
    layout["yaxis"]["tickprefix"] = "R$ "
    fig.update_layout(**layout)

    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
        key=key
    )
