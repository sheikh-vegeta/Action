import together
from typing import List, Dict, Any
from app.domain.external.llm import LLM

class TogetherLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        together.api_key = self.api_key

    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        response = together.Chat.create(
            model=self.model,
            messages=messages
        )
        return response
