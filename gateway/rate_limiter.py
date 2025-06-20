import redis.asyncio as redis
from fastapi import Request, Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# Rate limit settings
RATE_LIMIT = 10  # max requests
WINDOW = 60      # in seconds

# Redis client
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def is_rate_limited(token: str) -> bool:
    key = f"ratelimit:{token}"
    current = await redis_client.get(key)

    if current is None:
        # Set counter with expiry
        await redis_client.set(key, 1, ex=WINDOW)
        return False
    elif int(current) < RATE_LIMIT:
        await redis_client.incr(key)
        return False
    else:
        return True
