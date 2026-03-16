# core/agents/sales_agent.py

from .base_agent import BaseAgent
from services.data_service import DataService


class SalesAgent(BaseAgent):

    def run(self):

        data_service = DataService(self.context)
        kpis = data_service.get_kpis()

        analysis_type = self.context.get("analysis_type", "Resumo Executivo")

        prompt = f"""
        Tipo de análise: {analysis_type}

        Receita total: {kpis['revenue']}
        Total de pedidos: {kpis['orders']}

        Gere uma análise estratégica executiva baseada nesses dados reais.
        """

        return self.run_llm(prompt)