import os
import psutil
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
import time

app = FastAPI(
    title="Tool API",
    description="API for tools running inside the sandbox.",
    version="0.1.0",
)

# --- Security & Sandboxing ---
BASE_WORKSPACE_DIR = "/workspace"
if not os.path.exists(BASE_WORKSPACE_DIR):
    os.makedirs(BASE_WORKSPACE_DIR)

def resolve_path(path: str) -> str:
    """Resolve a user-provided path to an absolute path within the workspace."""
    abs_path = os.path.abspath(os.path.join(BASE_WORKSPACE_DIR, path))
    if not abs_path.startswith(BASE_WORKSPACE_DIR):
        raise HTTPException(status_code=403, detail="File access outside of workspace is not allowed.")
    return abs_path

# --- Rate Limiting ---
RATE_LIMIT_DURATION = 60  # seconds
RATE_LIMIT_REQUESTS = 15  # requests per duration
request_counts = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in request_counts:
        request_counts[client_ip] = []

    # Remove old timestamps
    now = time.time()
    request_counts[client_ip] = [t for t in request_counts[client_ip] if now - t < RATE_LIMIT_DURATION]

    # Check limit
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    request_counts[client_ip].append(now)
    response = await call_next(request)
    return response


# --- Tool Endpoints ---
class FileContent(BaseModel):
    content: str

@app.get("/files/")
def list_files(path: str = "."):
    safe_path = resolve_path(path)
    try:
        return os.listdir(safe_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Directory not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filepath:path}")
def read_file(filepath: str):
    safe_path = resolve_path(filepath)
    try:
        with open(safe_path, "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/files/{filepath:path}")
def write_file(filepath: str, file_content: FileContent):
    safe_path = resolve_path(filepath)
    try:
        with open(safe_path, "w") as f:
            f.write(file_content.content)
        return {"message": "File written successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shell/")
def run_shell_command(command: str):
    try:
        import subprocess
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30, cwd=BASE_WORKSPACE_DIR
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/")
def search(query: str):
    try:
        from googlesearch import search
        results = list(search(query, num_results=10))
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitor/")
def get_resource_usage():
    """Returns current CPU and RAM usage."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
    }
