# core/agents/base_agent.py

from core.llm.llm_config import get_llm


class BaseAgent:

    def __init__(self, context=None):
        self.context = context or {}
        self.llm = get_llm()

    def run_llm(self, prompt: str):

        # 🔥 CrewAI LLM padrão
        if hasattr(self.llm, "call"):
            return self.llm.call(prompt)

        # 🔥 Caso seja callable
        if callable(self.llm):
            return self.llm(prompt)

        raise Exception(
            f"LLM incompatível detectado: {type(self.llm)}"
        )