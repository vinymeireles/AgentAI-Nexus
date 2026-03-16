# core/llm/llm_config.py

import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm():
    return LLM(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )
