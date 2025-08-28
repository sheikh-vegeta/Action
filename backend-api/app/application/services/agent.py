import os
import json
import requests
from typing import AsyncGenerator, List, Dict

from app.core.llm_provider import get_llm_provider
from app.domain.models import Session, Message

# --- Environment Variables ---
TOOL_API_PORT = 8081
MODEL_ID = os.environ.get("MODEL_ID", "anthropic/claude-3-sonnet:free")

# --- Prompt Engineering ---
SYSTEM_PROMPT = """
You are a helpful AI assistant that can use a variety of tools to answer user questions.
You have access to the following tools:
- File: list, read, write files.
- Shell: execute shell commands.
- Search: perform a web search.

When you need to use a tool, respond with a JSON object with "thought" and "action" fields.
The "action" field should contain the tool name, the command to perform, and the arguments.
Example:
{
    "thought": "I need to see what files are in the current directory.",
    "action": {
        "tool": "File",
        "command": "list",
        "args": {"path": "."}
    }
}

If you have enough information to answer the user's question, respond with a JSON object with a "thought" and "final_answer" field.
Example:
{
    "thought": "I have the file list and can now answer the user.",
    "final_answer": "The files in the current directory are: ..."
}
"""

class AgentService:
    """
    The core logic for the PlanAct Agent.
    """
    def __init__(self):
        try:
            self.llm_provider = get_llm_provider()
            self.llm_client = self.llm_provider.get_client()
        except ValueError as e:
            print(f"LLM Provider Error: {e}")
            self.llm_client = None

    def _call_tool(self, sandbox_hostname: str, action: Dict) -> Dict:
        """Calls a tool in the tool-api."""
        tool = action.get("tool", "").lower()
        command = action.get("command", "").lower()
        args = action.get("args", {})

        try:
            if tool == "file":
                if command == "list":
                    response = requests.get(f"http://{sandbox_hostname}:{TOOL_API_PORT}/files/", params=args)
                elif command == "read":
                    response = requests.get(f"http://{sandbox_hostname}:{TOOL_API_PORT}/files/{args.get('path')}")
                elif command == "write":
                    response = requests.put(f"http://{sandbox_hostname}:{TOOL_API_PORT}/files/{args.get('path')}", json={"content": args.get("content")})
                else:
                    return {"error": f"Unknown file command: {command}"}
            elif tool == "shell":
                response = requests.post(f"http://{sandbox_hostname}:{TOOL_API_PORT}/shell/", params=args)
            elif tool == "search":
                response = requests.get(f"http://{sandbox_hostname}:{TOOL_API_PORT}/search/", params=args)
            else:
                return {"error": f"Unknown tool: {tool}"}

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    async def process_message(
        self, session: Session, user_message: Message
    ) -> AsyncGenerator[str, None]:
        if not self.llm_client:
            yield json.dumps({"event": "error", "data": "LLM provider not configured."})
            yield json.dumps({"event": "end", "data": ""})
            return

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend([msg.model_dump() for msg in session.conversation.messages])

        sandbox_hostname = session.sandbox_id

        for _ in range(5): # Limit the number of loops to prevent infinite cycles
            try:
                response = self.llm_client.ChatCompletion.create(
                    model=MODEL_ID,
                    messages=messages,
                    temperature=0,
                )
                response_text = response.choices[0].message['content']
            except Exception as e:
                yield json.dumps({"event": "error", "data": f"LLM API Error: {e}"})
                break

            try:
                response_json = json.loads(response_text)
                thought = response_json.get("thought")
                if thought:
                    yield json.dumps({"event": "thought", "data": thought})
                    messages.append({"role": "assistant", "content": response_text})

                if "action" in response_json:
                    action = response_json["action"]
                    yield json.dumps({"event": "tool_call", "data": action})

                    tool_result = self._call_tool(sandbox_hostname, action)
                    yield json.dumps({"event": "tool_result", "data": tool_result})

                    messages.append({"role": "system", "content": f"Tool result: {json.dumps(tool_result)}"})

                elif "final_answer" in response_json:
                    final_answer = response_json["final_answer"]
                    for char in final_answer:
                        yield json.dumps({"event": "message_chunk", "data": char})
                    break # End of processing

            except json.JSONDecodeError:
                # The LLM didn't respond with valid JSON, treat it as a final answer
                for char in response_text:
                    yield json.dumps({"event": "message_chunk", "data": char})
                break

        yield json.dumps({"event": "end", "data": ""})
