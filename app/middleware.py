from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from app.redis_client import r
from app.auth import get_api_key

RATE_LIMIT = 100
WINDOW_SECONDS = 60 

async def auth_and_rate_limit(request: Request, call_next):
    ### This function checks auth api key in the header
    ### and limits the usage to the rate limit
    api_key = request.headers.get("Authorization")

    expected_key = get_api_key()
    if api_key != expected_key:
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or missing API Key"}
        )

    redis_key = f"rate-limit:{api_key}"
    current = r.get(redis_key)

    if current and int(current) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded for this API key"}
        )

    pipe = r.pipeline()
    pipe.incr(redis_key, 1)
    pipe.expire(redis_key, WINDOW_SECONDS)
    pipe.execute()

    return await call_next(request)
