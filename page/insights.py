# page/insights.py

import streamlit as st
from core.agents.sales_agent import SalesAgent

def render_insights():

    st.title("📈 Insights Automáticos")

    agent = SalesAgent()
    insight = agent.run()

    st.markdown(insight)