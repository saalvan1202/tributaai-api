from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
           # Si el error viene de SQLAlchemy y tiene .orig
            if hasattr(e, "orig"):
                msg = str(e.orig)
                # si tiene DETAIL, lo extraes
                detail = msg.split("DETAIL:")[-1].strip()
            else:
                # error "normal" de Python
                detail = str(e)

            return JSONResponse(
                status_code=500,
                content={"error": detail}
            )