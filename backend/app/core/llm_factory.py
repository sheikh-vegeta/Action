import os
from app.domain.external.llm import LLM
from app.infrastructure.llm.openrouter import OpenRouterLLM
from app.infrastructure.llm.groq import GroqLLM
from app.infrastructure.llm.together import TogetherLLM
from app.infrastructure.llm.huggingface import HuggingFaceLLM
from ...infrastructure.llm.portkey import PortkeyLLM
from ...infrastructure.llm.cohere import CohereLLM

def get_llm() -> LLM:
    provider = os.environ.get("LLM_PROVIDER", "openrouter").lower()
    api_key = os.environ.get(f"{provider.upper()}_API_KEY")
    model = os.environ.get("MODEL_ID")

    if not api_key:
        raise ValueError(f"{provider.upper()}_API_KEY not set")
    if not model:
        raise ValueError("MODEL_ID not set")

    if provider == "openrouter":
        return OpenRouterLLM(api_key=api_key, model=model)
    elif provider == "groq":
        return GroqLLM(api_key=api_key, model=model)
    elif provider == "together":
        return TogetherLLM(api_key=api_key, model=model)
    elif provider == "huggingface":
        return HuggingFaceLLM(api_key=api_key, model=model)
    elif provider == "portkey":
        return PortkeyLLM(api_key=api_key, model=model)
    elif provider == "cohere":
        return CohereLLM(api_key=api_key, model=model)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
