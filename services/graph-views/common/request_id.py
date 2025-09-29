import os
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

REQ_ID_HEADER = os.getenv("IT_REQUEST_ID_HEADER", "X-Request-Id")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get(REQ_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers[REQ_ID_HEADER] = req_id
        return response
