"""KPI Cards - 8 metricas principais do dashboard."""
#components/kpi_cards.py

import streamlit as st
from data.olist_data import format_currency, format_number


KPI_CONFIG = [
    {"key": "total_revenue", "label": "Receita Total", "icon": "💰", "color": "emerald",
     "format": lambda v: format_currency(v)},
    {"key": "total_orders", "label": "Total de Pedidos", "icon": "🛒", "color": "amber",
     "format": lambda v: format_number(v)},
    {"key": "total_customers", "label": "Total de Clientes", "icon": "👥", "color": "sky",
     "format": lambda v: format_number(v)},
    {"key": "avg_ticket", "label": "Ticket Medio", "icon": "📈", "color": "rose",
     "format": lambda v: format_currency(v)},
    {"key": "avg_review", "label": "Avaliacao Media", "icon": "⭐", "color": "amber",
     "format": lambda v: f"{v:.1f} / 5.0"},
    {"key": "active_customers", "label": "Clientes Ativos", "icon": "✅", "color": "emerald",
     "format": lambda v: format_number(v)},
    {"key": "cancel_rate", "label": "Taxa Cancelamento", "icon": "❌", "color": "rose",
     "format": lambda v: f"{v}%"},
    {"key": "delivered_orders", "label": "Pedidos Entregues", "icon": "📦", "color": "sky",
     "format": lambda v: format_number(v)},
]


def render_kpi_cards(kpis: dict):
    """Renderiza os 8 KPI cards em 2 linhas de 4."""

    # Primeira linha - 4 KPIs
    cols = st.columns(4)
    for i, kpi in enumerate(KPI_CONFIG[:4]):
        with cols[i]:
            value = kpis[kpi["key"]]
            formatted = kpi["format"](value)
            st.markdown(f"""
            <div class="kpi-card kpi-{kpi['color']}">
                <div class="kpi-icon">{kpi['icon']}</div>
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value {kpi['color']}">{formatted}</div>
            </div>
            """, unsafe_allow_html=True)

    # Segunda linha - 4 KPIs
    cols2 = st.columns(4)
    for i, kpi in enumerate(KPI_CONFIG[4:]):
        with cols2[i]:
            value = kpis[kpi["key"]]
            formatted = kpi["format"](value)
            st.markdown(f"""
            <div class="kpi-card kpi-{kpi['color']}">
                <div class="kpi-icon">{kpi['icon']}</div>
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value {kpi['color']}">{formatted}</div>
            </div>
            """, unsafe_allow_html=True)
