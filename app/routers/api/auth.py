from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse
)

from app.schemas.common import MessageResponse
from app.services.auth_service import (
    login_user,
    register_user
)

from app.core.limiter import limiter


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db,
        credentials.email,
        credentials.password
    )


@router.post("/register", response_model=MessageResponse)
@limiter.limit("5/minute")
def register(
    request: Request,
    credentials: RegisterRequest,
    db: Session = Depends(get_db),
):
    register_user(
        db,
        credentials.username,
        credentials.email,
        credentials.password
    )

    return MessageResponse(message="Registration successful")
