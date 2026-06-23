from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi import Request

from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from app.core.logger import logger

from app.exceptions.base import (
    DomainError,
    RedirectException
)

from app.schemas.common import (
    ErrorResponse
)

templates = Jinja2Templates(
    directory="app/templates"
)

ERROR_STATUS = {
    "invalid_credentials": 401,
    "invalid_token": 401,
    "authentication_required": 401,

    "access_denied": 403,

    "user_exists": 409,
    "already_enrolled": 409,

    "user_not_found": 404,
    "role_not_found": 404,
    "course_not_found": 404,
    "lesson_not_found": 404,
}


def get_status(
    exc: DomainError
):
    return ERROR_STATUS.get(
        exc.code,
        400
    )


def is_api(
    request: Request
):
    return request.url.path.startswith(
        "/api"
    )


async def domain_exception_handler(
    request: Request,
    exc: DomainError
):
    status = get_status(
        exc
    )

    logger.warning(
        f"DOMAIN_ERROR | "
        f"path={request.url.path} | "
        f"code={exc.code}"
    )

    if is_api(
        request
    ):
        return JSONResponse(
            status_code=status,
            content=ErrorResponse(
                message=exc.message
            ).model_dump()
        )


    return templates.TemplateResponse(
        request=request,
        name=f"errors/{status}.html",
        context=ErrorResponse(
            message=exc.message
        ).model_dump(),
        status_code=status
    )
    

async def custom_http_exception_handler(
    request: Request,
    exc: Exception
):
    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        message = exc.detail
    elif isinstance(exc, RequestValidationError):
        status_code = 422
        message = "The address page or form contains uncorrected data."
    else:
        status_code = 500
        message = "Internal server error"

    logger.warning(
        f"HTTP_EXCEPTION | "
        f"path={request.url.path} | "  
        f"status={status_code} "
    )

    if is_api(request):
        if isinstance(exc, RequestValidationError):
            return JSONResponse(
                status_code=status_code,
                content=ErrorResponse(
                    message=exc.errors()[0]["msg"]
                ).model_dump()
            )

        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(
                message=message
            ).model_dump()
        )

    try:
        return templates.TemplateResponse(
            request=request,
            name=f"errors/{status_code}.html",
            context=ErrorResponse(
                message=message
            ).model_dump(),
            status_code=status_code
        )
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="errors/404.html",
            context=ErrorResponse(
                message=message
            ).model_dump(),
            status_code=status_code
        )


async def redirect_exception_handler(
    request: Request,
    exc: RedirectException
):
    return RedirectResponse(
        url=exc.url,
        status_code=exc.status_code
    )