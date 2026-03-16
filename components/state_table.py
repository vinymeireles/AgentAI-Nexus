"""Ranking por Estado - Versão com st.dataframe"""
# components/state_table.py


import streamlit as st
import pandas as pd
from data.olist_data import format_currency, format_number


def render_state_table(state_df: pd.DataFrame):
    """Renderiza ranking por estado usando st.dataframe."""

    #st.subheader("🏆 Ranking por Estado")
    #st.caption("Top 10 estados por receita")

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">🏆 Ranking por Estado</div>
        <div class="section-subtitle">Top 10 estados por receita</div>
    </div>
    """, unsafe_allow_html=True)



    if state_df is None or state_df.empty:
        st.info("Nenhum dado disponível.")
        return

    # Ordenar e pegar top 10
    top10 = (
        state_df
        .sort_values("revenue", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    # Criar coluna de ranking
    top10.insert(0, "Posição", top10.index + 1)

    # Garantir divisão segura
    max_revenue = top10["revenue"].max()
    if max_revenue == 0:
        max_revenue = 1

    # Criar coluna percentual para barra
    top10["Performance (%)"] = (top10["revenue"] / max_revenue) * 100

    # Renomear colunas para exibição
    display_df = top10.rename(columns={
        "state": "UF",
        "state_name": "Estado",
        "customers": "Clientes",
        "orders": "Pedidos",
        "revenue": "Receita",
        "avg_ticket": "Ticket Médio"
    })

    # Selecionar ordem final das colunas
    display_df = display_df[
        [
            "Posição",
            "UF",
            "Estado",
            "Clientes",
            "Pedidos",
            "Receita",
            "Ticket Médio",
            "Performance (%)"
        ]
    ]

    # Aplicar estilo
    styled_df = (
        display_df.style
        .format({
            "Clientes": lambda x: format_number(int(x)),
            "Pedidos": lambda x: format_number(int(x)),
            "Receita": lambda x: format_currency(x),
            "Ticket Médio": lambda x: format_currency(x),
        })
        .bar(
            subset=["Performance (%)"],
            align="left"
        )
    )

    st.dataframe(
        styled_df,
        width="stretch",
        hide_index=True
    )
