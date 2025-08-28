import groq
from typing import List, Dict, Any
from ...domain.external.llm import LLM

class GroqLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = groq.Groq(api_key=self.api_key)

    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
