
#data/auth.py

import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# data/auth.py

import streamlit as st
import base64
import os
from services.auth_service import AuthService

def authentication():

    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.user = None

    if not st.session_state.auth:

        st.markdown("<h2 style='text-align:center'>🔐 Autenticação</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray'>Acesso ao painel executivo inteligente</p>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            with st.container(border=True):

                if os.path.exists("assets/logo.png"):
                    b = base64.b64encode(open("assets/logo.png", "rb").read()).decode()
                    st.markdown(
                        f"<div style='text-align:center'><img src='data:image/png;base64,{b}' width='260'/></div>",
                        unsafe_allow_html=True
                    )

                tab1, tab2 = st.tabs(["Login", "Cadastro"])

                # LOGIN
                with tab1:
                    with st.form("login_form"):
                        email = st.text_input("Email")
                        password = st.text_input("Senha", type="password")
                        login_btn = st.form_submit_button("Entrar")

                        if login_btn:
                            success, response = AuthService.login_user(email, password)
                            if success:
                                st.session_state.auth = True
                                st.session_state.user = response
                                st.rerun()
                            else:
                                st.error(response)

                # CADASTRO
                with tab2:
                    with st.form("register_form"):
                        email = st.text_input("Email", key="reg_email")
                        password = st.text_input("Senha", type="password", key="reg_pass")
                        register_btn = st.form_submit_button("Cadastrar")

                        if register_btn:
                            success, message = AuthService.register_user(email, password)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)

        st.stop()