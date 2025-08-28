from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/")
def list_files(path: str = "."):
    try:
        return os.listdir(path)
    except Exception as e:
        return {"error": str(e)}

@router.get("/{filepath:path}")
def read_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        return {"error": str(e)}
