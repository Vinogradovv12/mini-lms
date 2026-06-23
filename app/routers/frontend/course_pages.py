from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from app.database import get_db

from app.dependencies.frontend.auth import get_current_actor_required
from app.authorization.permissions import can_manage_course, is_course_author, is_enrolled
from app.dependencies.frontend.permissions import require_course_creator, require_course_manager
from app.schemas.access import CourseAccess
from app.services.course_service import create_course, delete_course, get_course, update_course
from app.services.enrollment_service import enroll_user
from app.authorization.permissions import can_create_course
from app.dependencies.frontend.context import base_context



router = APIRouter(
    tags=["Frontend - Course Pages"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/courses/create")
def create_course_page(
    request: Request,
    db: Session = Depends(get_db),
    actor=Depends(
        require_course_creator
    )
):    
    return templates.TemplateResponse(
        request=request,
        name="create_course.html",
        context=base_context(
            request,
            current_user=actor
        )
    )


@router.post("/courses/create")
def create_course_form(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
    actor=Depends(
        get_current_actor_required
    )
):  
    create_course(
        db,
        title=title,
        description=description,
        actor=actor
    )

    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )


@router.get("/courses/{course_id}")
def course_page(
    course_id: int,
    request: Request,
    db: Session = Depends(get_db),
    actor=Depends(
        get_current_actor_required
    )
):
    course = get_course(
        db,
        course_id
    )

    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context=base_context(
            request,
            current_user=actor,
            course=course,
            is_enrolled=is_enrolled(db, actor, course),
            can_manage_course = can_manage_course(actor, course),
            is_author = is_course_author(actor, course)
        )
    )


@router.post("/courses/{course_id}/enroll")
def enroll_user_endpoint(
    course_id: int,
    request: Request,
    db: Session = Depends(get_db),
    actor=Depends(
        get_current_actor_required
    )
):
    enroll_user(
        db,
        course_id,
        actor
    )

    return RedirectResponse(
        url=f"/courses/{course_id}",
        status_code=302
    )


@router.get("/courses/{course_id}/edit")
def edit_course_page(
    request: Request,
    access: CourseAccess = Depends(
        require_course_manager
    )
):
    return templates.TemplateResponse(
        request=request,
        name="edit_course.html",
        context=base_context(
            request,
            course=access.course
        )
    )


@router.post("/courses/{course_id}/edit")
def edit_course(
    course_id:int,
    title:str=Form(...),
    description:str=Form(...),
    access: CourseAccess=Depends(
        require_course_manager
    ),
    db:Session=Depends(get_db)
):
    update_course(
        db,
        access.actor,
        course_id,
        title,
        description
    )

    return RedirectResponse(
        f"/courses/{course_id}",
        303
    )


@router.post("/courses/{course_id}/delete")
def delete_course_endpoint(
    course_id:int,
    access: CourseAccess=Depends(
        require_course_manager
    ),
    db:Session=Depends(get_db)
):
    delete_course(
        db,
        course_id,
        access.actor
    )

    return RedirectResponse(
        "/dashboard",
        303
    )