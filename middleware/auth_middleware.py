from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from security.security import verify_token

PUBLIC_PATHS = ["/api/v1/login/", "/docs", "/openapi.json"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rutas públicas
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth:
            return JSONResponse({"detail": "Token requerido"}, status_code=401)

        token = auth.split(" ")[1]
        payload = verify_token(token)

        if not payload:
            return JSONResponse({"detail": "Token inválido o expirado"}, status_code=401)

        request.state.user = payload
        return await call_next(request)
