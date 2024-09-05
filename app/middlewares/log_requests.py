from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import logger


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        body = await request.body()
        form = await request.form()
        message = f"[{request.method}]: {request.url} body: {body} headers: {request.headers} form: {form}"
        logger.info(message)
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"[{e}]: {message}")
            raise e
        return response
