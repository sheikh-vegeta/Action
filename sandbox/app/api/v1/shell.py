from fastapi import APIRouter
import subprocess

router = APIRouter()

@router.post("/run")
def run_command(command: str):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        return {"error": str(e)}
