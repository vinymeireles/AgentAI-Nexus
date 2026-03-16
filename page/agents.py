# page/agents.py

import streamlit as st
from datetime import datetime
import time

from core.executor import execute
from core.agents.sales_agent import SalesAgent
from core.agents.finance_agent import FinanceAgent
from core.agents.customer_agent import CustomerAgent
from core.agents.growth_agent import GrowthAgent

from services.metrics_service import get_metrics
from services.data_service import DataService

ds = DataService()

categories = ["Todos"] + ds.get_categories()
states = ["Todos"] + ds.get_states()
segments = ["Todos"] + ds.get_segments()

#Função dos agentes
def render_agents():

    # ==============================
    # AGENTS MAP (NOVO PADRÃO)
    # ==============================
    AGENTS = [
        {
            "id": "sales",
            "name": "Agente de Vendas",
            "icon": "📊",
            "description": "Análise estratégica de vendas com base em dados reais.",
            "class": SalesAgent
        },
        {
            "id": "finance",
            "name": "Agente Financeiro",
            "icon": "💰",
            "description": "Análise financeira executiva.",
            "class": FinanceAgent
        },
        {
            "id": "customer",
            "name": "Agente de Clientes",
            "icon": "👥",
            "description": "Análise comportamental e retenção de clientes.",
            "class": CustomerAgent
        },
        {
            "id": "growth",
            "name": "Agente de Crescimento",
            "icon": "🚀",
            "description": "Análise estratégica de expansão e crescimento.",
            "class": GrowthAgent
        },
    ]

    # ==============================
    # SESSION STATE INIT
    # ==============================
    if "agent_status" not in st.session_state:
        st.session_state.agent_status = {
            agent["id"]: "Pronto" for agent in AGENTS
        }

    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []

    # ==============================
    # HEADER
    # ==============================
    st.title("🤖 Hub de Agentes IA")
    st.markdown(
        "<span style='color:#6B7280'>Execute agentes individualmente para gerar relatórios inteligentes</span>",
        unsafe_allow_html=True
    )

    st.divider()

    # ==============================
    # FILTROS GLOBAIS
    # ==============================
    with st.expander("⚙️ Filtros de Análise", expanded=False):

        col1, col2, col3, col4 = st.columns(4)

        # =============================
        # PERÍODO
        # =============================
        with col1:
            period = st.selectbox(
                "Período",
                [
                    "Últimos 7 dias",
                    "Últimos 30 dias",
                    "Este mês",
                    "Este ano",
                    "Personalizado"
                ]
            )

        # =============================
        # SEGMENTO (customers.segment)
        # =============================
        with col2:
            segment = st.selectbox(
                "Segmento",
                segments
            )

        # =============================
        # CATEGORIA (products.category)
        # =============================
        with col3:
            category = st.selectbox(
                "Categoria",
                categories
            )

        # =============================
        # ESTADO (customers.state)
        # =============================
        with col4:
            state = st.selectbox(
                "Estado",
                states
            )

        # =============================
        # PERÍODO PERSONALIZADO
        # =============================
        if period == "Personalizado":
            col5, col6 = st.columns(2)
            with col5:
                start_date = st.date_input("Data Inicial")
            with col6:
                end_date = st.date_input("Data Final")
        else:
            start_date = None
            end_date = None

        # =============================
        # TIPO DE ANÁLISE (PROMPT)
        # =============================
        analysis_type = st.selectbox(
            "Tipo de Análise",
            [
                "Resumo Executivo",
                "Análise Detalhada",
                "Análise Estratégica"
            ]
        )

    st.divider()

    # ==============================
    # GRID 4 COLUNAS
    # ==============================
    cols = st.columns(4)

    for idx, agent in enumerate(AGENTS):

        col = cols[idx % 4]

        with col:
            with st.container(border=True):

                status = st.session_state.agent_status.get(agent["id"], "Pronto")

                st.markdown(f"### {agent['icon']} {agent['name']}")
                st.caption(f"Status: {status}")
                st.write(agent["description"])

                st.divider()

                # ==============================
                # BOTÃO EXECUTAR
                # ==============================
                if status == "Pronto":

                    if st.button(
                        "▶️ Executar",
                        key=f"run_{agent['id']}"
                    ):

                        st.session_state.agent_status[agent["id"]] = "Executando"

                        with st.spinner("🧠 Executando análise inteligente..."):

                            # Contexto (ainda não injetado no agente — futura evolução)
                            context = {
                                "period": period,
                                "segment": segment,
                                "product": category,
                                "state": state,
                                "start_date": start_date,
                                "end_date": end_date,
                                "analysis_type": analysis_type
                            }

                            context["analysis_type"] = analysis_type

                            # ✅ NOVO EXECUTOR PADRÃO
                            agent_class = agent["class"]
                            insight, pdf_path = execute(agent_class, context)

                            time.sleep(2)

                            st.success("✅ Relatório gerado com sucesso!")

                            # 🔥 Salva histórico
                            st.session_state.agent_history.append({
                                "agent_id": agent["id"],
                                "pdf_path": pdf_path,
                                "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
                            })

                        st.session_state.agent_status[agent["id"]] = "Pronto"
                        st.rerun()

                elif status == "Executando":
                    st.button(
                        "⏳ Executando...",
                        disabled=True,
                        key=f"executando_{agent['id']}"
                    )

    # ==============================
    # AVISO SOBRE RELATÓRIOS
    # ==============================

    st.divider()

    st.info("📌 Os relatórios gerados ficam disponíveis na página de Relatórios.")

    if st.button("📂 Ir para Relatórios", key="go_to_reports_agents"):
        st.query_params["page"] = "Relatórios"
        st.rerun()