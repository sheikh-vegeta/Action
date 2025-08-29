import json
import os
import asyncio
from typing import Dict, Any

class MCPService:
    """
    Service for managing Model Context Protocol (MCP) servers.
    """
    def __init__(self, config_path="mcp_config.json"):
        self.config = self._load_config(config_path)
        self.active_servers: Dict[str, asyncio.subprocess.Process] = {}

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {"mcpServers": {}}

    def get_available_tools(self) -> Dict[str, Any]:
        tools = {}
        for name, server in self.config.get("mcpServers", {}).items():
            if server.get("enabled"):
                tools[name] = server.get("description", "No description available.")
        return tools

    async def start_server(self, name: str) -> bool:
        """Starts an MCP server as a subprocess if it's stdio-based."""
        if name in self.active_servers and self.active_servers[name].returncode is None:
            return True # Already running

        server_config = self.config.get("mcpServers", {}).get(name)
        if not server_config or server_config.get("transport") != "stdio":
            return False

        command = server_config.get("command")
        args = server_config.get("args", [])

        try:
            process = await asyncio.create_subprocess_exec(
                command, *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            self.active_servers[name] = process
            return True
        except Exception as e:
            print(f"Failed to start MCP server '{name}': {e}")
            return False

    async def send_request(self, server_name: str, request_data: Dict) -> Dict:
        """Sends a request to a running stdio-based MCP server."""
        if server_name not in self.active_servers or self.active_servers[server_name].returncode is not None:
            if not await self.start_server(server_name):
                return {"error": f"MCP server '{server_name}' is not running and could not be started."}

        process = self.active_servers[server_name]

        try:
            request_str = json.dumps(request_data) + "\n"
            process.stdin.write(request_str.encode())
            await process.stdin.drain()

            response_str = await process.stdout.readline()
            if not response_str:
                return {"error": "No response from MCP server."}

            return json.loads(response_str)
        except Exception as e:
            return {"error": f"Error communicating with MCP server '{server_name}': {e}"}

    async def stop_all_servers(self):
        """Terminates all active MCP server subprocesses."""
        for name, process in self.active_servers.items():
            if process.returncode is None:
                process.terminate()
                await process.wait()
                print(f"Stopped MCP server '{name}'.")
