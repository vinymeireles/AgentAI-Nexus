#page/admin_auth.py

import streamlit as st
from services.supabase_client import supabase_admin as supabase
from services.auth_service import AuthService


def render_admin_auth():

    if "user" not in st.session_state:
        st.stop()

    user = st.session_state.user

    if user["role"] != "admin":
        st.error("Acesso restrito ao administrador.")
        st.stop()

    st.title("🔐 Controle de Autenticação")

    tab1, tab2 = st.tabs(["Usuários Pendentes", "Usuários Ativos"])

    # ================= PENDENTES =================
    with tab1:
        response = supabase.table("users") \
            .select("*") \
            .eq("status", "pendente") \
            .execute()

        users = response.data

        if not users:
            st.success("Nenhum usuário pendente.")
        else:
            for u in users:
                col1, col2 = st.columns([3,1])

                col1.write(f"📧 {u['email']}")

                if col2.button("Aprovar", key=u["id"]):
                    AuthService.approve_user(u["id"])
                    st.success("Usuário aprovado com sucesso ✅")
                    st.rerun()

    # ================= ATIVOS =================
    with tab2:
        response = supabase.table("users") \
            .select("*") \
            .eq("status", "ativo") \
            .execute()

        users = response.data

        if not users:
            st.info("Nenhum usuário ativo.")
        else:
            for u in users:
                st.write(f"📧 {u['email']}")