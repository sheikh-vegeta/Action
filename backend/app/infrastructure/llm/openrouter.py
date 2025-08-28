import openai
from typing import List, Dict, Any
from ...domain.external.llm import LLM

class OpenRouterLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
