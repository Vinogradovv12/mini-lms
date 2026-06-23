from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.lesson import(
    LessonCreate,
    LessonPreviewResponse,
    LessonResponse
)

from app.dependencies.api.auth import get_current_actor

from app.services.lesson_service import create_lesson, get_lesson_by_id, get_lessons_by_course_id


router = APIRouter(
    prefix="/api/lessons",
    tags=["Lessons"]
)


@router.post("/courses/{course_id}", response_model=LessonResponse)
def create_lesson_endpoint(
    course_id: int, 
    data: LessonCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_actor)
):
    return create_lesson(
        db=db,
        actor=current_user,
        course_id=course_id,
        title=data.title,
        description=data.description,
        content=data.content
    )


@router.get("/course/{course_id}", response_model=list[LessonPreviewResponse])
def get_course_lesson_endpoint(
    course_id: int,
    db: Session = Depends(get_db)
):
    return get_lessons_by_course_id(
        db=db,
        course_id=course_id
    )


@router.get("{lesson_id}", response_model=LessonResponse)
def get_lesson_by_id_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
    actor = Depends(get_current_actor)
):
    return get_lesson_by_id(
        db,
        lesson_id,
        actor
    )