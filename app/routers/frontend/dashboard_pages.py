from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db


from app.dependencies.api.auth import require_admin
from app.dependencies.frontend.auth import get_current_actor_required, require_admin_page
from app.dependencies.frontend.auth import (
    get_current_actor_optional
)

from app.models.user import User
from app.services.course_service import (
    get_dashboard_courses,
    list_public_courses
)

from app.dependencies.frontend.context import base_context
from app.services.user_service import get_users_data


router = APIRouter(
    tags=["Frontend - Dashboard Pages"]
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
):
    actor = get_current_actor_optional(
        request,
        db
    )

    if actor:
        return RedirectResponse(
            url="/dashboard",
            status_code=302
        )

    courses = list_public_courses(
        db
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=base_context(
            request,
            courses=courses
        )
    )


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    actor=Depends(
        get_current_actor_required
    )
):
    dashboard_data = get_dashboard_courses(
        db,
        actor.id
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=base_context(
            request,
            current_user=actor,
            **dashboard_data
        )
    )


@router.get("/admin")
def admin_panel(
    request: Request,
    db: Session = Depends(get_db),
    actor=Depends(
        require_admin_page
    )
):
    users_data = get_users_data(
        db
    )

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context=base_context(
            request,
            actor,
            users=users_data
        )
    )