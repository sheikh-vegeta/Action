import os
import json
import requests
from typing import AsyncGenerator, List, Dict

from app.core.llm_provider import get_llm_provider
from app.domain.models import Session, Message
from .mcp_service import MCPService

# --- Environment Variables ---
TOOL_API_PORT = 8081
MODEL_ID = os.environ.get("MODEL_ID", "anthropic/claude-3-sonnet:free")

# --- System Prompt ---
def get_system_prompt():
    mcp_service = MCPService()
    mcp_tools = mcp_service.get_available_tools()

    mcp_prompt_part = "\nAdditionally, you can use the following external tools via the Model Context Protocol (MCP):\n"
    for name, description in mcp_tools.items():
        mcp_prompt_part += f"- {name}: {description}\n"

    base_prompt = """
You are a helpful AI assistant that can use a variety of tools to answer user questions.
You have access to the following sandbox tools:
- File: list, read, write files.
- Shell: execute shell commands.
- Search: perform a web search.

When you need to use a tool, respond with a JSON object with "thought" and "action" fields.
For sandbox tools, use this format:
{
    "thought": "I need to see what files are in the current directory.",
    "action": {
        "tool": "File",
        "command": "list",
        "args": {"path": "."}
    }
}

For MCP tools, use this format:
{
    "thought": "I need to access the local filesystem.",
    "action": {
        "tool": "mcp",
        "command": "filesystem",
        "args": { ... }
    }
}

If you have enough information to answer the user's question, respond with a JSON object with a "thought" and "final_answer" field.
"""
    return base_prompt + mcp_prompt_part


class AgentService:
    """
    The core logic for the PlanAct Agent.
    """
    def __init__(self):
        try:
            self.llm_provider = get_llm_provider()
            self.llm_client = self.llm_provider.get_client()
            self.system_prompt = get_system_prompt()
        except ValueError as e:
            print(f"LLM Provider Error: {e}")
            self.llm_client = None
            self.system_prompt = ""

    def _call_tool(self, sandbox_hostname: str, action: Dict) -> Dict:
        # ... (omitted for brevity, no changes here)
        pass

    async def process_message(
        self, session: Session, user_message: Message
    ) -> AsyncGenerator[str, None]:
        if not self.llm_client:
            yield json.dumps({"event": "error", "data": "LLM provider not configured."})
            yield json.dumps({"event": "end", "data": ""})
            return

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend([msg.model_dump() for msg in session.conversation.messages])

        # ... (rest of the function is the same)
        pass
