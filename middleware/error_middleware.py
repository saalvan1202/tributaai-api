from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": str(str(e.orig).split("DETAIL:")[-1].strip())}
            )