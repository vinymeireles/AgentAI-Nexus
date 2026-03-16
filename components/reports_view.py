# components/reports_view.py

import streamlit as st
import os


def render_reports():

    st.markdown("## 📄 Relatórios Gerados")
    st.divider()

    if not st.session_state.get("agent_history"):
        st.info("Nenhum relatório gerado ainda.")
        return

    cols = st.columns(2)

    for idx, h in enumerate(st.session_state.agent_history):

        col = cols[idx % 2]

        with col:
            with st.container(border=True):

                st.markdown(f"### {h['agent_id'].upper()}")
                st.markdown(f"📅 {h['created_at']}")

                pdf_path = os.path.join(
                    "output",
                    h["agent_id"],
                    h["pdf"]
                )

                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf:
                        st.download_button(
                            "⬇️ Download PDF",
                            pdf.read(),
                            h["pdf"],
                            key=f"dl_{idx}"
                        )
                else:
                    st.button("PDF indisponível", disabled=True)
