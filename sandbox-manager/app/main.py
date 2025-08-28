import docker
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Sandbox Manager API",
    description="API for managing Docker sandboxes.",
    version="0.1.0",
)

client = docker.from_env()

@app.post("/sandboxes/", status_code=201)
def create_sandbox(image: str = "ubuntu:latest", command: str = "sleep 3600"):
    """
    Create a new sandbox (Docker container).
    """
    try:
        container = client.containers.run(image, command, detach=True)
        return {"id": container.id, "name": container.name, "status": container.status}
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=f"Image '{image}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sandboxes/{sandbox_id}")
def get_sandbox(sandbox_id: str):
    """
    Get information about a sandbox.
    """
    try:
        container = client.containers.get(sandbox_id)
        return {"id": container.id, "name": container.name, "status": container.status}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Sandbox not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sandboxes/{sandbox_id}", status_code=204)
def delete_sandbox(sandbox_id: str):
    """
    Stop and remove a sandbox.
    """
    try:
        container = client.containers.get(sandbox_id)
        container.stop()
        container.remove()
        return
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Sandbox not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
