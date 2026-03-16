# services/insight_service.py

from core.orchestrator import OrchestratorAgent


class InsightService:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()

    def generate_sales_insight(self):
        return self.orchestrator.run("sales")

    def generate_finance_insight(self):
        return self.orchestrator.run("finance")

