from huggingface_hub import InferenceClient
from typing import List, Dict, Any
from ...domain.external.llm import LLM

class HuggingFaceLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = InferenceClient(model=self.model, token=self.api_key)

    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        response = self.client.chat_completion(
            messages=messages,
            max_tokens=500, # This might need to be configurable
        )
        return response
