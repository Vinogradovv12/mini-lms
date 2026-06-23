from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Form

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.dependencies.frontend.context import base_context
from app.schemas.auth import RegisterForm, RegisterRequest
from app.services.auth_service import login_user, register_user
from app.dependencies.frontend.auth import get_current_actor_optional

from app.core.limiter import limiter
from app.database import get_db


router = APIRouter(
    tags=["Frontend - Auth Pages"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/login")
def login_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=base_context(request)
    )

@router.post("/login")
@limiter.limit("10/minute")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    token = login_user(
        db,
        email,
        password
    )


    if not token:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context=base_context(
                request=request,
                error="Invalid email or password"
            )
        )
    
    response = RedirectResponse(
        url="/dashboard",
        status_code=302
    )
    
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return response

@router.get("/logout")
def logout():
    respone = RedirectResponse(
        url="/",
        status_code=302
    )

    respone.delete_cookie(
        "access_token"
    )

    return respone

@router.get("/register")
def register_page(
    request: Request,
    db: Session = Depends(get_db)
):
    actor = get_current_actor_optional(
        request,
        db
    )

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context=base_context(
            request,
            actor
        )
    )


@router.post("/register")
@limiter.limit("5/minute")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        credentials = RegisterRequest(
            username=username,
            email=email,
            password=password
        )

        register_user(
            db,
            credentials.username,
            credentials.email,
            credentials.password
        )

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    except ValidationError as e:

        error = e.errors()[0]["msg"]

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context=base_context(
                request,
                error=error,
                username=username,
                email=email
            ),
            status_code=422
        )