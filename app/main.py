import os

from fastapi import FastAPI
import uvicorn

from app.core.exception_registery import register_exception_handlers
from app.database import Base, engine

from app.models import *

from app.routers.frontend.course_pages import router as course_pages_router
from app.routers.frontend.auth_pages import router as auth_pages_router
from app.routers.frontend.dashboard_pages import router as dashboard_pages_router
from app.routers.frontend.lesson_pages import router as lesson_pages_router
from app.routers.api.role import router as role_router
from app.routers.api.user import router as user_router
from app.routers.api.auth import router as auth_router
from app.routers.api.course import router as course_router
from app.routers.api.lesson import router as lesson_router
from app.routers.api.enrollment import router as enrollment_router

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.exceptions.base import DomainError
from app.core.exception_handlers import domain_exception_handler

from app.core.limiter import limiter


app = FastAPI()

app.include_router(course_pages_router)
app.include_router(auth_pages_router)
app.include_router(dashboard_pages_router)
app.include_router(lesson_pages_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(lesson_router)
app.include_router(enrollment_router)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

register_exception_handlers(app)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9090))
    uvicorn.run(app, host="0.0.0.0", port=port)