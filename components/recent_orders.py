"""Pedidos Recentes - Lista dos ultimos pedidos registrados."""
#components/recent_orders.py

import streamlit as st
import pandas as pd
from data.olist_data import format_currency, PAYMENT_LABELS


STATUS_BADGES = {
    "entregue": "badge-entregue",
    "enviado": "badge-enviado",
    "processando": "badge-processando",
    "cancelado": "badge-cancelado",
}

STATUS_LABELS = {
    "entregue": "Entregue",
    "enviado": "Enviado",
    "processando": "Processando",
    "cancelado": "Cancelado",
}


def _render_stars(score) -> str:
    if pd.isna(score):
        return '<div style="margin-top:3px; height:10px;"></div>'

    s = max(0, min(5, int(score)))

    filled = ''.join(['<span class="star-dot star-filled"></span>'] * s)
    empty = ''.join(['<span class="star-dot star-empty"></span>'] * (5 - s))

    return f'<div style="margin-top:3px;">{filled}{empty}</div>'





def render_recent_orders(orders_df: pd.DataFrame, limit: int = 10):
    """Renderiza lista de pedidos recentes."""

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Pedidos Recentes</div>
        <div class="section-subtitle">Ultimos pedidos registrados</div>
    </div>
    """, unsafe_allow_html=True)

    recent = orders_df.sort_values("order_date", ascending=False).head(limit)

    for _, order in recent.iterrows():

        status = str(order["status"]).strip().lower()

        badge_class = STATUS_BADGES.get(status, "badge-processando")
        badge_label = STATUS_LABELS.get(status, status.capitalize())

        pm_label = PAYMENT_LABELS.get(order["payment_method"], order["payment_method"])
        stars = _render_stars(order.get("review_score"))


        # Formatar data
        try:
            parts = order["order_date"].split("-")
            date_str = f"{parts[2]}/{parts[1]}/{parts[0]}"
        except Exception:
            date_str = order["order_date"]

        st.markdown(f"""
        <div class="order-item">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="order-id">{order['id']}</span>
                    <span class="badge {badge_class}">{badge_label}</span>
                </div>
                <div class="order-name">{order['customer_name']}</div>
                <div class="order-detail">{order['product_category']} &mdash; {pm_label}</div>
            </div>
            <div style="text-align: right;">
                <div class="order-value">{format_currency(order['total_value'])}</div>
                <div class="order-date">{date_str}</div>
                {stars}
            </div>
        </div>
        """, unsafe_allow_html=True)
