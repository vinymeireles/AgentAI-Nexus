# core/executor.py

from datetime import datetime
import os
from utils.pdf import generate_pdf
from services.db import save_report


AGENT_MAP = {
    "sales": "core.agents.sales_agent.SalesAgent",
    "finance": "core.agents.finance_agent.FinanceAgent",
    "customer": "core.agents.customer_agent.CustomerAgent",
    "growth": "core.agents.growth_agent.GrowthAgent",
}


def execute(agent_class, context=None):

    # Agora o agente recebe contexto
    agent = agent_class(context=context)

    result = agent.run()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("output", exist_ok=True)
    pdf_path = f"output/report_{timestamp}.pdf"

    generate_pdf(result, pdf_path)
    save_report(agent.__class__.__name__, result, pdf_path)

    return result, pdf_path