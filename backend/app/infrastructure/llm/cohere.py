import cohere
from typing import List, Dict, Any
from ...domain.external.llm import LLM

class CohereLLM(LLM):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = cohere.Client(self.api_key)

    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        # Cohere's API has a different message format. We need to adapt it.
        # This is a simplified adaptation.
        prompt = messages[-1]["content"] # Use the last user message as the prompt

        return self.client.chat(
            model=self.model,
            message=prompt,
            # conversation_history would go here if we built it
        )
