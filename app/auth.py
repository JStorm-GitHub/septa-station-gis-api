from fastapi import Request, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
import os

API_KEY_PATH = os.path.join(os.path.dirname(__file__), "../shared/api_key.txt")

def get_api_key():
    try:
        with open(API_KEY_PATH) as f:
            return f.read().strip()
    except FileNotFoundError:
        raise RuntimeError("API key file not found.")

def verify_api_key(request: Request):
    api_key = request.headers.get("Authorization")
    if api_key != get_api_key():
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )