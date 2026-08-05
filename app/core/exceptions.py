import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger("api_exceptions")


async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for Pydantic input validation errors."""
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err["loc"]])
        errors.append({"field": field, "message": err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "status_code": 422,
            "message": "Input validation error",
            "errors": errors,
        },
    )


async def global_unhandled_exception_handler(request: Request, exc: Exception):
    """Custom fallback handler for uncaught server exceptions."""
    logger.error(f"Unhandled Internal Server Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status_code": 500,
            "message": "An internal server error occurred. Please try again later.",
        },
    )
