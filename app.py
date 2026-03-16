"""
AgentAI Nexus CRM Dashboard - Aplicacao Principal Streamlit
====================================================
Dashboard CRM moderno com dados simulados do ecommerce NexMarket.
Pronto para deploy no Streamlit Cloud.

Para rodar localmente no VSCode:
    cd streamlit_app
    pip install -r requirements.txt
    streamlit run app.py
"""


import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

### Bibliotecas
import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime
from streamlit_option_menu import option_menu
from crewai import Agent, Task, Crew, Process
from data.auth import authentication
from page.admin_auth import render_admin_auth

# Nexus Agents Core
from services.db import init_db


from components.reports_view import render_reports

# ==========================================
# SESSION STATE INIT
# ==========================================
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {
        "sales": "Pronto",
        "finance": "Pronto",
        "executive": "Pronto",
    }

if "agent_history" not in st.session_state:
    st.session_state.agent_history = []


# ---------------------------------------------------------------------------
# Page Config (DEVE ser a primeira chamada Streamlit)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AgentAI Nexus",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS Injection
# ---------------------------------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "assets/style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



#função de autenticação - Login e Senha
authentication()

# Inicializa banco de relatórios Nexus
init_db()

# Garantir pasta de saída
os.makedirs("output", exist_ok=True)

# ==========================================================
# SESSION STATE GLOBAL DOS AGENTES
# ==========================================================
if "agent_status" not in st.session_state:
    st.session_state.agent_status = {
        "sales": "Pronto",
        "finance": "Pronto"
    }



# ==========================================================
# SIDEBAR MENU — NAVEGAÇÃO POR PÁGINAS
# ==========================================================
with st.sidebar:
    st.image("assets/logo.png", width='content')

    st.markdown("""
    <div style='text-align:center;color:#9CA3AF;font-size:13px;margin-bottom:20px'>
    Business Intelligence com Agentes Autônomos
    </div>
    """, unsafe_allow_html=True)

    # ---------------- MENU DINÂMICO ----------------
    user = st.session_state.user

    options = [
        "Dashboard",
        "Agentes IA",
        "Insights",
        "Chat CRM",
        "Relatórios",
        "Sobre"
    ]

    icons = [
        "bar-chart-fill",
        "cpu-fill",
        "check-circle-fill",
        "chat-dots-fill",
        "file-earmark-text-fill",
        "info-circle-fill"
    ]

    # 👑 Adiciona painel admin apenas se for administrador
    if user["role"] == "admin":
        options.append("Controle de Usuários")
        icons.append("shield-lock-fill")

    # Sempre deixar sair por último
    options.append("Sair")
    icons.append("box-arrow-right")

    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent"
            },
            "icon": {
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "padding": "10px 14px",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background-color": "#2563EB",
                "font-weight": "600",
            },
        }
    )

    # ---------------- INFO USUÁRIO ----------------
    st.markdown(
        f"👤 **{user['email']}**  \n"
        f"🔑 Perfil: `{user['role'].upper()}`"
    )

    st.divider()


# ---------------- LOGOUT ----------------
if selected == "Sair":
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()


# ---------------- QUERY PARAM ----------------
query_page = st.query_params.get("page")

if query_page:
    selected = query_page
    st.query_params.clear()


# ---------------------------------------------------------------------------
# Controlar paginas do Sistema
# --------------------------------------------------------------------------
if selected == "Dashboard":
    from page.dashboards import render_dashboard
    render_dashboard()

elif selected == "Agentes IA":
    from page.agents import render_agents
    render_agents()

elif selected == "Relatórios":
    from page.reports import render_reports
    render_reports()

elif selected == "Chat CRM":
    from page.chat import render_chat
    render_chat()

elif selected == "Insights":
    from page.insights import render_insights
    render_insights()

elif selected == "Sobre":
    from page.sobre import render_sobre
    render_sobre()

elif selected == "Controle de Usuários":
    render_admin_auth()    

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="dashboard-footer">
    NexMarket CRM Dashboard &mdash; Dados da NexMarket| Ecommerce Brasil 2025
</div>
""", unsafe_allow_html=True)


#st.info("Desenvolvido por [VIMEUP](https://www.vimeup.com)")