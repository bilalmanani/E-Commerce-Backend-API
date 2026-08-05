import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts incoming HTTP requests, logs method/path,
    and measures total execution processing time in milliseconds.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}ms"
        
        logger.info(
            f"Method={request.method} Path={request.url.path} "
            f"Status={response.status_code} Duration={formatted_process_time}"
        )
        
        response.headers["X-Process-Time"] = formatted_process_time
        return response
