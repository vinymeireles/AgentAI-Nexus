#total_registry.py

from .kpi_tool import get_kpis_summary
from .state_tool import get_top_states
from .revenue_tool import get_last_months_revenue


class ToolRegistry:

    def __init__(self, data):
        self.data = data

    def execute(self, tool_name: str):

        if tool_name == "kpis":
            return get_kpis_summary(self.data)

        if tool_name == "top_states":
            return get_top_states(self.data)

        if tool_name == "revenue_trend":
            return get_last_months_revenue(self.data)

        return {"error": "Tool não encontrada"}