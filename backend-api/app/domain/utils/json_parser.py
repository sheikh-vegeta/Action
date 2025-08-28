import json
from typing import Any, Dict

class JsonParser:
    def parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Handle cases where the LLM might not produce perfect JSON
            # This is a simple implementation; a more robust one could use regex or other heuristics
            return {"error": "Invalid JSON format"}
