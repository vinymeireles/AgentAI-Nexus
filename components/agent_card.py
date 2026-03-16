# components/agent_card.py

import streamlit as st
from core.executor import execute_agent


def render_agent_card(agent, idx):

    agent_id = agent["id"]
    status = st.session_state.agent_status.get(agent_id, "Pronto")

    with st.container(border=True):

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="font-size:28px;">{agent['icon']}</div>
            <div>
                <b>{agent['nome']}</b>
                <div style="font-size:12px;color:gray;">{status}</div>
            </div>
        </div>

        <p style="font-size:14px;color:#6B7280">
            {agent['descricao']}
        </p>

        <b>CAPACIDADES</b>
        <ul>
            {''.join([f"<li>{c}</li>" for c in agent['capacidades']])}
        </ul>
        """, unsafe_allow_html=True)

        if status == "Pronto":
            if st.button("▶️ Ativar", key=f"run_{agent_id}_{idx}", width="content"):
                execute_agent(agent_id)

        elif status == "Executando":
            st.button("⏳ Executando...", disabled=True, key=f"exec_{idx}", width="content")

        else:
            st.button("✅ Executado", disabled=True, key=f"done_{idx}", width="content")
