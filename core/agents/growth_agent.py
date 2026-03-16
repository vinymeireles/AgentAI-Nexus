# core/agents/growth_agent.py

from .base_agent import BaseAgent
from services.data_service import DataService


class GrowthAgent(BaseAgent):

    def run(self):

        ds = DataService(self.context)

        top_states = ds.get_top_states()

        analysis_type = self.context.get("analysis_type", "Resumo Executivo")

        prompt = f"""
        Tipo de análise: {analysis_type}

        Estados com maior faturamento:
        {top_states.to_dict()}

        Gere uma análise estratégica de expansão
        e oportunidades regionais.
        """

        return self.run_llm(prompt)