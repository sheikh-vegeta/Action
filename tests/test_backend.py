from fastapi.testclient import TestClient


def get_app():
    # Import within function to ensure package resolution when tests run
    from app.main import app

    return app


def test_create_session():
    app = get_app()
    client = TestClient(app)

    resp = client.post("/sessions/")
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["user_id"] == "default_user"
    assert data["status"].lower() == "running"


def test_chat_sse_echoes_message():
    app = get_app()
    client = TestClient(app)

    # Create a session first
    session_id = client.post("/sessions/").json()["id"]

    # Stream chat SSE, ensure assistant echoes the message
    with client.stream(
        "POST",
        f"/sessions/{session_id}/chat",
        params={"message": "hello world"},
    ) as r:
        assert r.status_code == 200
        # Collect a few lines from the SSE stream
        lines = []
        for line in r.iter_lines():
            if not line:
                continue
            if isinstance(line, bytes):
                line = line.decode()
            lines.append(line)
            if len(lines) > 5:
                break

    body = "\n".join(lines)
    assert "Echo: hello world" in body
