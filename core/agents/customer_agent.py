# core/agents/customer_agent.py

from .base_agent import BaseAgent
from services.data_service import DataService


class CustomerAgent(BaseAgent):

    def run(self):

        ds = DataService(self.context)

        total_customers = ds.get_customers_count()
        active_customers = ds.get_active_customers()

        analysis_type = self.context.get("analysis_type", "Resumo Executivo")

        prompt = f"""
        Tipo de análise: {analysis_type}

        Total de clientes: {total_customers}
        Clientes ativos: {active_customers}

        Gere uma análise estratégica sobre retenção,
        engajamento e oportunidades de crescimento da base.
        """

        return self.run_llm(prompt)