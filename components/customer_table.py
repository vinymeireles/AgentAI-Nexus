"""Tabela de Clientes - Com busca, filtros e paginacao."""
#components/customer_table.py

import streamlit as st
import pandas as pd
from data.olist_data import format_currency, BRAZILIAN_STATES

PAGE_SIZE = 12


def render_customer_table(
    customers_df: pd.DataFrame,
    selected_state: str,
    selected_segment: str,
    selected_status: str,
):
    """Renderiza tabela de clientes com busca e paginacao."""

    # Filtros aplicados
    df = customers_df.copy()
    if selected_state != "Todos":
        df = df[df["state"] == selected_state]
    if selected_segment != "Todos":
        df = df[df["segment"] == selected_segment.lower()]
    if selected_status != "Todos":
        df = df[df["status"] == selected_status.lower()]

    # Busca
    search = st.text_input(
        "Buscar cliente",
        placeholder="Buscar por nome, email, ID ou cidade...",
        key="customer_search",
    )
    if search.strip():
        q = search.lower()
        df = df[
            df["name"].str.lower().str.contains(q, na=False) |
            df["email"].str.lower().str.contains(q, na=False) |
            df["id"].str.lower().str.contains(q, na=False) |
            df["city"].str.lower().str.contains(q, na=False)
        ]

    total = len(df)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    # Paginacao
    if "customer_page" not in st.session_state:
        st.session_state.customer_page = 0

    # Reset de pagina quando filtros mudam
    page = st.session_state.customer_page
    if page >= total_pages:
        page = 0
        st.session_state.customer_page = 0

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    paged = df.iloc[start:end]

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">Clientes</div>
        <div class="section-subtitle">{total} clientes encontrados</div>
    </div>
    """, unsafe_allow_html=True)

    if total == 0:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: var(--text-muted);">
            Nenhum cliente encontrado com os filtros atuais.
        </div>
        """, unsafe_allow_html=True)
        return

    # =========================
    # Tabela usando st.dataframe
    # =========================

    table_df = paged.copy()

    # Nome + Email em coluna única (mantém visual organizado)
    table_df["Nome"] = table_df["name"] + " (" + table_df["email"] + ")"

    # Estado com nome completo
    table_df["Estado"] = table_df["state"] + " - " + table_df["state"].map(
        lambda x: BRAZILIAN_STATES.get(x, x)
    )

    # Formatação
    table_df["Total Gasto"] = table_df["total_spent"].apply(format_currency)
    table_df["Pedidos"] = table_df["total_orders"]

    # Selecionar e renomear colunas finais
    table_df = table_df[[
        "id",
        "Nome",
        "city",
        "Estado",
        "Pedidos",
        "Total Gasto",
        "status",
        "segment"
    ]].rename(columns={
        "id": "ID",
        "city": "Cidade",
        "status": "Status",
        "segment": "Segmento"
    })

    st.dataframe(
        table_df,
        width="stretch",
        hide_index=True
    )


    # Paginacao
    if total_pages > 1:
        st.markdown(f"""
        <div class="pagination-container">
            <div class="pagination-info">Pagina {page + 1} de {total_pages}</div>
        </div>
        """, unsafe_allow_html=True)

        col_prev, col_pages, col_next = st.columns([1, 4, 1])
        with col_prev:
            if st.button("< Anterior", key="prev_page", disabled=(page == 0)):
                st.session_state.customer_page = max(0, page - 1)
                st.rerun()
        with col_next:
            if st.button("Proxima >", key="next_page", disabled=(page >= total_pages - 1)):
                st.session_state.customer_page = min(total_pages - 1, page + 1)
                st.rerun()
        with col_pages:
            # Numero de paginas (slider)
            if total_pages > 2:
                new_page = st.slider(
                    "Pagina",
                    1, total_pages, page + 1,
                    key="page_slider",
                    label_visibility="collapsed",
                )
                if new_page - 1 != page:
                    st.session_state.customer_page = new_page - 1
                    st.rerun()
