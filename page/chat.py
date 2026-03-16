# page/chat.py

import streamlit as st
import time
from core.orchestrator import OrchestratorAgent

CACHE_VERSION = "v3_postgres_sql"


def render_chat():

    st.title("💬 Chat CRM Inteligente")
    st.caption("Assistente estratégico conectado aos dados reais do CRM 📊")

    # ==================================================
    # 🔐 INICIALIZAÇÃO SESSION STATE
    # ==================================================
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "response_times" not in st.session_state:
        st.session_state.response_times = []

    if "chat_cache" not in st.session_state:
        st.session_state.chat_cache = {}

    if "preset_question" not in st.session_state:
        st.session_state.preset_question = None

    orchestrator = OrchestratorAgent()

    # ==================================================
    # 📈 MÉTRICA MÉDIA DE PERFORMANCE
    # ==================================================
    if len(st.session_state.response_times) > 0:
        avg_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
        st.metric("⏱️ Tempo médio de resposta", f"{round(avg_time, 2)}s")

    # ==================================================
    # 🧠 EXPANDER COM PERGUNTAS CLICÁVEIS
    # ==================================================
    with st.expander("🧠 Perguntas Estratégicas", expanded=False):

        def question_button(label):
            if st.button(label, use_container_width=True):
                st.session_state.preset_question = label

        # ----------------------------
        # 📊 VENDAS
        # ----------------------------
        st.markdown("##### 📊 Vendas & Receita")
        col1, col2, col3 = st.columns(3)

        with col1:
            question_button("Faturamento último mês")
            question_button("Faturamento por estado")

        with col2:
            question_button("Comparar jan x fev")
            question_button("Mês com maior volume")

        with col3:
            question_button("Crescimento últimos 3 meses")
            question_button("Receita por forma pagamento")

        # ----------------------------
        # 👥 CLIENTES
        # ----------------------------
        st.markdown("##### 👥 Clientes")
        col1, col2, col3 = st.columns(3)

        with col1:
            question_button("Clientes ativos")
            question_button("Top 10 clientes")

        with col2:
            question_button("Clientes compra única")
            question_button("Clientes inativos +60 dias")

        with col3:
            question_button("Maior ticket médio")
            question_button("Clientes por estado")

        # ----------------------------
        # 📦 PRODUTOS
        # ----------------------------
        st.markdown("##### 📦 Produtos")
        col1, col2, col3 = st.columns(3)

        with col1:
            question_button("Produtos mais vendidos")

        with col2:
            question_button("Categorias mais lucrativas")

        with col3:
            question_button("Produtos sem vendas 30 dias")

        # ----------------------------
        # 📈 INDICADORES
        # ----------------------------
        st.markdown("##### 📈 Indicadores")
        col1, col2, col3 = st.columns(3)

        with col1:
            question_button("Ticket médio geral")

        with col2:
            question_button("Taxa de recompra")

        with col3:
            question_button("Tendência de crescimento")

    # ==================================================
    # 💬 INPUT DO CHAT
    # ==================================================
    user_input = st.chat_input(
        "Faça uma pergunta estratégica sobre o desempenho do seu CRM ou utilize as sugestões acima..."
    )

    # Se clicou em botão
    if st.session_state.preset_question:
        user_input = st.session_state.preset_question
        st.session_state.preset_question = None

    # ==================================================
    # 🚀 PROCESSAMENTO
    # ==================================================
    if user_input:

        cache_key = f"{CACHE_VERSION}:{user_input}"

        # ==========================
        # ⚡ CACHE INTELIGENTE VERSIONADO
        # ==========================
        if cache_key in st.session_state.chat_cache:
            response = st.session_state.chat_cache[cache_key]
            processing_time = 0

        else:
            start_time = time.time()

            with st.spinner("🔎 Analisando dados e gerando insight estratégico..."):
                response = orchestrator.run(user_input)

            end_time = time.time()
            processing_time = round(end_time - start_time, 2)

            # salva no cache versionado
            st.session_state.chat_cache[cache_key] = response

            # salva tempo para média
            st.session_state.response_times.append(processing_time)

        # ==========================
        # 🎯 BADGE PERFORMANCE
        # ==========================
        if processing_time == 0:
            badge = "⚡ Resposta instantânea (cache)"
        elif processing_time < 2:
            badge = "🟢 Excelente performance"
        elif 2 <= processing_time <= 4:
            badge = "🟡 Performance moderada"
        else:
            badge = "🔴 Processamento elevado"

        response_with_time = (
            f"{response}\n\n"
            f"---\n"
            f"{badge}\n"
            f"⏱️ Tempo de processamento: {processing_time}s"
        )

        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response_with_time))

    # ==================================================
    # 💬 HISTÓRICO
    # ==================================================
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    # ==================================================
    # 🧹 LIMPAR CONVERSA
    # ==================================================
    if st.sidebar.button("🧹 Limpar Conversa"):
        st.session_state.chat_history = []
        st.session_state.response_times = []
        st.session_state.chat_cache = {}
        st.session_state.preset_question = None
        st.rerun()