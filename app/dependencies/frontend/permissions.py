from fastapi import Depends, HTTPException

from app.database import get_db
from app.dependencies.frontend.auth import (
    get_current_actor_required
)

from app.schemas.access import CourseAccess, LessonAccess
from app.services.course_service import get_course

from app.authorization.permissions import (
    can_manage_course,
    can_create_course,
    can_access_course
)
from app.services.lesson_service import get_lesson_by_id


def require_course_creator(
    actor=Depends(get_current_actor_required)
):
    if not can_create_course(actor):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return actor


def require_course_manager(
    course_id: int,
    db=Depends(get_db),
    actor=Depends(get_current_actor_required)
):
    course = get_course(
        db,
        course_id
    )

    if not can_manage_course(
        actor,
        course
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return CourseAccess(
        actor=actor,
        course=course
    )


def require_course_access(
    lesson_id: int,
    db=Depends(get_db),
    actor=Depends(get_current_actor_required)
):
    lesson = get_lesson_by_id(
        db,
        lesson_id,
        actor
    )

    if not can_access_course(
        db,
        actor,
        lesson.course
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return LessonAccess(
        actor=actor,
        lesson=lesson
    )