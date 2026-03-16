"""Status dos Pedidos - Cards de status com contagem."""
#components/order_status.py

import streamlit as st
import pandas as pd


STATUS_CONFIG = [
    {"key": "entregue", "label": "Entregue", "icon": "📦", "icon_class": "emerald"},
    {"key": "enviado", "label": "Enviado", "icon": "🚚", "icon_class": "sky"},
    {"key": "processando", "label": "Processando", "icon": "⏳", "icon_class": "amber"},
    {"key": "cancelado", "label": "Cancelado", "icon": "❌", "icon_class": "rose"},
]


def render_order_status(status_df: pd.DataFrame):
    """Renderiza cards de status dos pedidos."""

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Status dos Pedidos</div>
        <div class="section-subtitle">Distribuicao atual por status</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, cfg in enumerate(STATUS_CONFIG):
        row = status_df[status_df["status"] == cfg["key"]]
        count = int(row["count"].values[0]) if len(row) > 0 else 0
        pct = float(row["percentage"].values[0]) if len(row) > 0 else 0.0

        with cols[i % 2]:
            st.markdown(f"""
            <div class="status-card">
                <div class="status-icon status-icon-{cfg['icon_class']}">
                    {cfg['icon']}
                </div>
                <div>
                    <div class="status-label">{cfg['label']}</div>
                    <div class="status-count">{count}</div>
                    <div class="status-percent">{pct}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
