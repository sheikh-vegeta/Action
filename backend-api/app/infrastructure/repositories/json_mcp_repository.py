import json
import os
from typing import Dict, Any
from app.domain.repositories.mcp_repository import MCPRepository

class JsonMCPRepository(MCPRepository):
    def __init__(self, config_path="mcp_config.json"):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the MCP configuration file."""
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {"mcpServers": {}}

    def get_available_tools(self) -> Dict[str, Any]:
        """Returns a dictionary of available MCP tools and their descriptions."""
        tools = {}
        for name, server in self.config.get("mcpServers", {}).items():
            if server.get("enabled"):
                tools[name] = server.get("description", "No description available.")
        return tools
