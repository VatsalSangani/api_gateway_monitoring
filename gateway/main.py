from fastapi import FastAPI, Request
from starlette.responses import Response
from starlette.status import HTTP_502_BAD_GATEWAY
import httpx
from middleware import RateLimitMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
import subprocess
from pydantic import BaseModel

app = FastAPI()

# Initialize Prometheus instrumentation
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True
)
instrumentator.instrument(app).expose(app, endpoint="/metrics")

# Register custom middleware
app.add_middleware(RateLimitMiddleware)

# Service routing table
SERVICE_MAP = {
    "service1": "http://mock_service:8001"
}

@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        return Response(content=f"Unknown service: {service}", status_code=404)

    target_url = f"{SERVICE_MAP[service]}/{path}"

    async with httpx.AsyncClient() as client:
        for attempt in range(3):  # 1 attempt + 2 retries
            try:
                proxied_response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=request.headers.raw,
                    content=await request.body(),
                    timeout=5.0
                )

                # Retry only on server errors (5xx), not on 4xx
                if proxied_response.status_code >= 500:
                    await asyncio.sleep(0.5 * (attempt + 1))
                    continue

                return Response(
                    content=proxied_response.content,
                    status_code=proxied_response.status_code,
                    headers=dict(proxied_response.headers)
                )

            except httpx.RequestError:
                await asyncio.sleep(0.5 * (attempt + 1))  # Retry on connection issues

    return Response(content="Service unavailable after retries", status_code=HTTP_502_BAD_GATEWAY)

class RestartRequest(BaseModel):
    service_name: str

@app.post("/admin/restart_service")
async def restart_service(req: RestartRequest):
    valid_services = {"mock_service"}
    if req.service_name not in valid_services:
        return {"error": "Invalid service name"}

    try:
        result = subprocess.run(
            ["docker", "restart", f"api_gateway_project-{req.service_name}-1"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}
    except Exception as e:
        return {"status": "error", "output": str(e)}