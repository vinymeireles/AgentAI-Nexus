# core/agents/finance_agent.py

from .base_agent import BaseAgent
from services.data_service import DataService


class FinanceAgent(BaseAgent):

    def run(self):

        ds = DataService(self.context)
        kpis = ds.get_kpis()

        revenue = kpis["revenue"]
        expenses = revenue * 0.6  # simulação
        profit = revenue - expenses

        analysis_type = self.context.get("analysis_type", "Resumo Executivo")

        prompt = f"""
        Tipo de análise: {analysis_type}

        Receita: {revenue}
        Despesas estimadas: {expenses}
        Lucro estimado: {profit}

        Gere análise financeira estratégica.
        """

        return self.run_llm(prompt)