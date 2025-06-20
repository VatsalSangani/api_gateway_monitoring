from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from rate_limiter import is_rate_limited

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for Prometheus metrics endpoint
        if request.url.path.startswith("/metrics"):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            return Response(content="Missing Authorization token", status_code=400)

        token = token.replace("Bearer ", "")

        if await is_rate_limited(token):
            return Response(content="Rate limit exceeded", status_code=HTTP_429_TOO_MANY_REQUESTS)

        return await call_next(request)
