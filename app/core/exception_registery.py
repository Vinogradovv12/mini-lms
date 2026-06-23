from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.base import (
    DomainError,
    RedirectException
)

from app.core.exception_handlers import (
    domain_exception_handler,
    custom_http_exception_handler,
    redirect_exception_handler
)


def register_exception_handlers(
    app: FastAPI
):
    app.add_exception_handler(
        DomainError,
        domain_exception_handler
    )

    app.add_exception_handler(
        StarletteHTTPException,
        custom_http_exception_handler
    )

    app.add_exception_handler(
        RequestValidationError,
        custom_http_exception_handler
    )

    app.add_exception_handler(
        RedirectException,
        redirect_exception_handler
    )