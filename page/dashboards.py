# page/dashboards.py

from components.kpi_cards import render_kpi_cards
from components.revenue_chart import render_revenue_chart
from components.orders_chart import render_orders_chart
from components.category_chart import render_category_chart
from components.payment_chart import render_payment_chart
from components.order_status import render_order_status
from components.state_table import render_state_table
from components.customer_table import render_customer_table
from components.recent_orders import render_recent_orders
import streamlit as st

from data.database import (
    load_customers,
    load_orders,
    load_payments,
)

from data.olist_data import (
    get_kpis,
    get_monthly_revenue,
    get_category_data,
    get_payment_data,
    get_state_data,
    get_order_status_counts,
    get_all_states,
    BRAZILIAN_STATES,
)


@st.cache_data(ttl=300)
def load_all_data():
    """Carrega dados do Supabase"""

    customers_df = load_customers()
    orders_df = load_orders()
    payments_df = load_payments()

    return {
        "customers": customers_df,
        "orders": orders_df,
        "payments_raw": payments_df,
        "kpis": get_kpis(customers_df, orders_df),
        "monthly": get_monthly_revenue(orders_df),
        "categories": get_category_data(orders_df),
        "payments": get_payment_data(orders_df),
        "states": get_state_data(orders_df),
        "order_status": get_order_status_counts(orders_df),
        "all_states": get_all_states(customers_df),
    }


data = load_all_data()


def render_dashboard():
    st.markdown("""
    <div class="dashboard-header">
        <div class="header-title">
            📊 NexMarket CRM Dashboard
            <span class="header-live-badge">
                <span class="live-dot"></span>
                Ao Vivo
            </span>
        </div>
        <div class="header-subtitle">Painel de gestao de clientes e pedidos - Ecommerce NexMarket 2025</div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <div style="padding: 8px 0 16px 0;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 700; color: #e2e8f0;">
                📊 Análise CRM
            </div>
            <div style="font-size: 0.78rem; color: #5a6b8a; margin-top: 2px;">Filtros e Configuracoes</div>
        </div>
        """, unsafe_allow_html=True)

        state_options = ["Todos"] + [f"{s} - {BRAZILIAN_STATES[s]}" for s in data["all_states"]]
        selected_state_raw = st.selectbox("Estado", state_options, index=0, key="filter_state")
        selected_state = selected_state_raw.split(" - ")[0] if selected_state_raw != "Todos" else "Todos"

        selected_segment = st.selectbox(
            "Segmento",
            ["Todos", "Premium", "Regular", "Ocasional"],
            index=0,
            key="filter_segment",
        )

        selected_status = st.selectbox(
            "Status do Cliente",
            ["Todos", "Ativo", "Inativo", "Novo"],
            index=0,
            key="filter_status",
        )

        st.markdown("---")

        st.markdown("""
        <div style="padding: 12px 0;">
            <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: #5a6b8a; font-weight: 500; margin-bottom: 8px;">
                Resumo Rapido
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Clientes", f"{data['kpis']['total_customers']}")
        with col_b:
            st.metric("Pedidos", f"{data['kpis']['total_orders']}")

        col_c, col_d = st.columns(2)
        with col_c:
            st.metric("Ativos", f"{data['kpis']['active_customers']}")
        with col_d:
            st.metric("Cancel.", f"{data['kpis']['cancel_rate']}%")

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #5a6b8a; text-align: center; padding: 8px 0;">
            Dados analisados<br>
            NexMarket Ecommerce Brasil 2025
        </div>
        """, unsafe_allow_html=True)

    filtered_orders = data["orders"]
    if selected_state != "Todos" and "state" in data["orders"].columns:
        filtered_orders = data["orders"][data["orders"]["state"] == selected_state]

    filtered_context = {
        "kpis": data["kpis"],
        "orders": filtered_orders,
        "states": get_state_data(filtered_orders),
        "monthly": get_monthly_revenue(filtered_orders),
        "order_status": get_order_status_counts(filtered_orders),
        "customers": data["customers"],
    }

    st.session_state["dashboard_data"] = filtered_context

    tab_overview, tab_clientes, tab_pedidos, tab_estados = st.tabs([
        "Visao Geral",
        "Clientes",
        "Pedidos",
        "Estados",
    ])

    with tab_overview:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        render_kpi_cards(data["kpis"])
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        col_rev, col_ord = st.columns(2)
        with col_rev:
            render_revenue_chart(data["monthly"], key="revenue_overview")
        with col_ord:
            render_orders_chart(data["monthly"])

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        col_cat, col_pay, col_status = st.columns(3)
        with col_cat:
            render_category_chart(data["categories"], key="category_overview")
        with col_pay:
            render_payment_chart(data["payments"], key="payment_overview")
        with col_status:
            render_order_status(data["order_status"])

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        col_state, col_recent = st.columns(2)
        with col_state:
            render_state_table(data["states"])
        with col_recent:
            render_recent_orders(data["orders"], limit=8)

    with tab_clientes:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        render_customer_table(
            data["customers"],
            selected_state,
            selected_segment,
            selected_status,
        )

    with tab_pedidos:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

        col_st, col_pm = st.columns(2)
        with col_st:
            filtered_status = (
                get_order_status_counts(filtered_orders)
                if len(filtered_orders) > 0
                else data["order_status"]
            )
            render_order_status(filtered_status)

        with col_pm:
            render_payment_chart(data["payments"], key="payment_orders")

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        render_recent_orders(filtered_orders, limit=12)

    with tab_estados:
        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
        render_state_table(data["states"])

        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

        col_cat2, col_rev2 = st.columns(2)
        with col_cat2:
            render_category_chart(data["categories"], key="category_states")
        with col_rev2:
            render_revenue_chart(data["monthly"], key="revenue_states")