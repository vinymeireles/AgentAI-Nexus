# page/reports.py

import streamlit as st
import os
from datetime import datetime, timedelta
from services.db import get_reports

# ===============================================
# AGENTS MAP LOCAL (SUBSTITUI agent_registry)
# ===============================================

AGENTS = [
    {
        "id": "sales",
        "name": "Agente de Vendas",
        "icon": "📊"
    },
    {
        "id": "finance",
        "name": "Agente Financeiro",
        "icon": "💰"
    },
    {
        "id": "customer",
        "name": "Agente de Clientes",
        "icon": "👥"
    },
    {
        "id": "growth",
        "name": "Agente de Crescimento",
        "icon": "🚀"
    },
]

# ==========================================================
# RELATÓRIOS — DASHBOARD EXECUTIVO
# ==========================================================
def render_reports():

    # ======================================================
    # SESSION STATE
    # ======================================================
    if "hide_reports" not in st.session_state:
        st.session_state.hide_reports = False

    # ======================================================
    # HEADER
    # ======================================================
    h1, h2 = st.columns([3, 2])

    with h1:
        st.markdown("## 📄 Relatórios")
        st.markdown(
            "<span style='color:#6B7280'>Relatórios executivos gerados pelos agentes de IA</span>",
            unsafe_allow_html=True
        )

    with h2:
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Resetar Filtros", help="Resetar os filtros de pesquisas", use_container_width=True):
            st.session_state.hide_reports = False
            st.rerun()
            

    st.divider()

    # ======================================================
    # FILTROS RÁPIDOS DE PERÍODO
    # ======================================================
    st.markdown("### 📆 Período")

    c1, c2, c3 = st.columns(3)

    today = datetime.today().date()

    if c1.button("Hoje", use_container_width=True):
        start_date = today
        end_date = today
    elif c2.button("7 dias", use_container_width=True):
        start_date = today - timedelta(days=7)
        end_date = today
    elif c3.button("30 dias", use_container_width=True):
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data Inicial", value=today - timedelta(days=7))
        with col2:
            end_date = st.date_input("Data Final", value=today)

    st.divider()

    # ======================================================
    # FILTRO POR AGENTE + BUSCA
    # ======================================================
    f1, f2 = st.columns(2)

    with f1:
        agent_options = ["Todos"] + [a["name"] for a in AGENTS]
        selected_agent = st.selectbox("🤖 Filtrar por agente", agent_options)

    with f2:
        keyword = st.text_input("🔎 Buscar por palavra-chave")

    st.divider()

    # ======================================================
    # BUSCAR RELATÓRIOS
    # ======================================================
    reports = get_reports()

    if not reports:
        st.info("⚠️ Nenhum relatório encontrado.")
        return

    if st.session_state.hide_reports:
        st.warning("⚠️ Nenhum relatório sendo exibido. Execute novamente o login do sistema para visualizar os relatórios do banco!")
        return

    # ======================================================
    # FILTRAGEM
    # ======================================================
    filtered_reports = []

    for r in reports:
        _, agent_id, insight, pdf_path, created_at = r

        try:
            report_datetime = datetime.strptime(created_at, "%d/%m/%Y %H:%M")
            report_date = report_datetime.date()
        except:
            continue

        # Filtro por período
        if not (start_date <= report_date <= end_date):
            continue

        # Filtro por agente
        if selected_agent != "Todos":
            agent_info = next((a for a in AGENTS if a["id"] == agent_id), None)
            if not agent_info or agent_info["name"] != selected_agent:
                continue

        # Filtro por palavra-chave
        if keyword:
            if keyword.lower() not in insight.lower():
                continue

        filtered_reports.append(r)

    # ======================================================
    # RESULTADOS
    # ======================================================
    if not filtered_reports:
        st.info("Nenhum relatório corresponde aos filtros aplicados.")
        return

    st.metric("📊 Relatórios encontrados", len(filtered_reports))

    st.divider()

    # ======================================================
    # GRID 2 COLUNAS
    # ======================================================
    cols = st.columns(2)

    for idx, r in enumerate(filtered_reports):

        _, agent_id, insight, pdf_path, created_at = r
        col = cols[idx % 2]

        with col:
            with st.container(border=True):

                agent_info = next(
                    (a for a in AGENTS if a["id"] == agent_id),
                    None
                )

                agent_name = agent_info["name"] if agent_info else agent_id
                agent_icon = agent_info["icon"] if agent_info else "🤖"

                st.markdown(f"### {agent_icon} {agent_name}")

                st.markdown(
                    f"""
                    <span style='
                        background:#EEF2FF;
                        color:#3730A3;
                        padding:4px 10px;
                        border-radius:999px;
                        font-size:12px'>
                        {agent_id.upper()}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p style='font-size:12px;color:#9CA3AF'>📅 {created_at}</p>",
                    unsafe_allow_html=True
                )

                st.divider()

                with st.expander("📑 Visualizar resumo"):
                    preview = insight[:800] + "..." if len(insight) > 800 else insight
                    st.markdown(preview)

                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Baixar PDF",
                            f.read(),
                            file_name=os.path.basename(pdf_path),
                            key=f"pdf_{idx}",
                            use_container_width=True
                        )
                else:
                    st.button(
                        "📄 PDF indisponível",
                        disabled=True,
                        key=f"no_pdf_{idx}",
                        use_container_width=True
                    )

    st.divider()
