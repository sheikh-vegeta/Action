import os
import docker
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Sandbox Manager API",
    description="API for managing Docker sandboxes.",
    version="0.1.0",
)

client = docker.from_env()
SANDBOX_IMAGE_TAG = "sandbox-image:latest"
COMPOSE_NETWORK_NAME = os.environ.get("COMPOSE_NETWORK_NAME")

def build_sandbox_image():
    """Builds the sandbox image if it doesn't exist."""
    try:
        client.images.get(SANDBOX_IMAGE_TAG)
    except docker.errors.ImageNotFound:
        try:
            print(f"Building sandbox image: {SANDBOX_IMAGE_TAG}")
            # Note: The 'path' should be relative to where the docker-compose command is run.
            client.images.build(
                path=".",
                dockerfile="./sandbox-image/Dockerfile",
                tag=SANDBOX_IMAGE_TAG,
                rm=True
            )
        except docker.errors.BuildError as e:
            raise HTTPException(status_code=500, detail=f"Failed to build sandbox image: {e}")

@app.on_event("startup")
async def startup_event():
    build_sandbox_image()

@app.post("/sandboxes/", status_code=201)
def create_sandbox():
    """
    Create a new sandbox (Docker container) and connect it to the compose network.
    """
    if not COMPOSE_NETWORK_NAME:
        raise HTTPException(status_code=500, detail="COMPOSE_NETWORK_NAME environment variable not set.")

    try:
        container = client.containers.run(
            SANDBOX_IMAGE_TAG,
            detach=True,
            network=COMPOSE_NETWORK_NAME,
        )
        container.reload()
        return {
            "id": container.id,
            "name": container.name, # The container name can be used as a hostname on the docker network
            "status": container.status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sandboxes/{sandbox_id}")
def get_sandbox(sandbox_id: str):
    """
    Get information about a sandbox.
    """
    try:
        container = client.containers.get(sandbox_id)
        container.reload()
        # The container name is the hostname
        return {
            "id": container.id,
            "name": container.name,
            "status": container.status,
        }
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
