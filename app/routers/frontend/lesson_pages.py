from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Form

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.frontend.auth import get_current_actor_required

from app.dependencies.frontend.permissions import require_course_access, require_course_manager
from app.services.lesson_service import (
    create_lesson,
)

from app.dependencies.frontend.context import base_context


router = APIRouter(
    tags=["Frontend - Lesson Pages"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/courses/{course_id}/lessons/create")
def create_lesson_page(
    course_id: int,
    request: Request,
    db: Session = Depends(get_db),
    access=Depends(
        require_course_manager
    )
):
    return templates.TemplateResponse(
        request=request,
        name="create_lesson.html",
        context=base_context(
            request,
            current_user=access.actor,
            course=access.course
        )
    )


@router.post("/courses/{course_id}/lessons/create")
def create_lesson_endpoint(
    course_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    actor=Depends(
        get_current_actor_required
    )    
):
    create_lesson(
        db=db,
        actor=actor,
        course_id=course_id,
        title=title,
        description=description,
        content=content
    )

    return RedirectResponse(
        url=f"/courses/{course_id}",
        status_code=302
    )


@router.get("/lessons/{lesson_id}")
def lesson_page(
    lesson_id: int,
    request: Request,
    db: Session = Depends(get_db),
    access=Depends(
        require_course_access
    )
):
    return templates.TemplateResponse(
        request=request,
        name="lesson.html",
        context=base_context(
            request,
            current_user=access.actor,
            lesson=access.lesson,
            course=access.lesson.course
        )
    )