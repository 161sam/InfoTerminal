from fastapi import Request


async def tenant_context_middleware(request: Request, call_next):
    request.state.tenant_id = request.headers.get("X-Tenant-Id", "default")
    return await call_next(request)
