import os
import openai
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def get_client(self):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_client(self):
        openai.api_key = self.api_key
        openai.api_base = "https://api.openai.com/v1"
        return openai

class OpenRouterProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_client(self):
        openai.api_key = self.api_key
        openai.api_base = "https://openrouter.ai/api/v1"
        return openai

def get_llm_provider() -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    """
    provider_name = os.environ.get("LLM_PROVIDER", "openai").lower()

    if provider_name == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set.")
        return OpenRouterProvider(api_key)

    elif provider_name == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        return OpenAIProvider(api_key)

    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
