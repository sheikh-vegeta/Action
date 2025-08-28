import asyncio
import requests
import websockets
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from app.application.services import SessionService
from app.domain.models import User
from .routes import get_current_user

# --- Environment Variables ---
SANDBOX_MANAGER_URL = os.environ.get("SANDBOX_MANAGER_URL", "http://sandbox-manager:8080")

router = APIRouter()
session_service = SessionService()

async def websocket_proxy(client_ws: WebSocket, target_uri: str):
    """Relay messages between a client and a target websocket."""
    try:
        async with websockets.connect(target_uri) as server_ws:
            async def forward(source, dest):
                while True:
                    try:
                        # Using bytes to support binary frames from VNC
                        message = await source.receive_bytes()
                        await dest.send_bytes(message)
                    except (WebSocketDisconnect, websockets.exceptions.ConnectionClosed):
                        break

            client_to_server = asyncio.create_task(forward(client_ws, server_ws))
            server_to_client = asyncio.create_task(forward(server_ws, client_ws))
            await asyncio.gather(client_to_server, server_to_client)
    except Exception as e:
        print(f"Websocket proxy connection failed: {e}")


@router.websocket("/vnc/{session_id}")
async def vnc_websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    ticket: str,
    current_user: User = Depends(get_current_user),
):
    """
    Proxies a WebSocket connection to the VNC server of a sandbox.
    Requires a valid, one-time ticket for access.
    """
    await websocket.accept()

    session = session_service.get_session(session_id)
    if not session or session.owner_id != current_user.username:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid session or ownership.")
        return

    if not session_service.validate_vnc_ticket(session_id, ticket):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired VNC ticket.")
        return

    try:
        response = requests.get(f"{SANDBOX_MANAGER_URL}/sandboxes/{session.sandbox_id}")
        response.raise_for_status()
        sandbox_data = response.json()
        # The sandbox container name is its hostname on the docker network
        sandbox_hostname = sandbox_data.get("name")
        if not sandbox_hostname:
            raise HTTPException(detail="Sandbox hostname not found.")
    except (requests.exceptions.RequestException, HTTPException) as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason=f"Failed to get sandbox details: {e}")
        return

    # websockify in the sandbox is running on port 6080
    vnc_uri = f"ws://{sandbox_hostname}:6080"
    try:
        await websocket_proxy(websocket, vnc_uri)
    except Exception as e:
        print(f"VNC proxy error: {e}")
    finally:
        await websocket.close()
