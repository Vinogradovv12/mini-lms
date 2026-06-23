from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.common import MessageResponse
from app.schemas.course import(
    CourseCreate,
    CourseResponse
) 

from app.services.course_service import(
    create_course, 
    get_course,
    list_public_courses,
    update_course,
    delete_course
)

from app.dependencies.api.auth import get_current_actor

router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"]
)

@router.post("/", response_model=CourseResponse)
def create_course_endpoint(
    data: CourseCreate,
    db: Session = Depends(get_db),
    actor = Depends(get_current_actor)
):
    return create_course(
        db=db,
        title=data.title,
        description=data.description,
        actor=actor
    )


@router.get("/", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db)
):
    return list_public_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_endpoint(
    course_id: int,
    db: Session = Depends(get_db),
):
    return get_course(
        db,
        course_id
    )


@router.put("/{course_id}", response_model=CourseResponse)
def update_course_endpoint(
    course_id: int,
    data: CourseCreate,
    db: Session = Depends(get_db),
    actor = Depends(get_current_actor)
):
    return update_course(
        db,
        course_id,
        title=data.title,
        description=data.description,
        actor=actor
    )


@router.delete("/{course_id}", response_model=MessageResponse)
def delete_course_endpoint(
    course_id: int,
    db: Session = Depends(get_db),
    actor = Depends(get_current_actor)
):
    delete_course(
        db,
        course_id,
        actor=actor
    )

    return MessageResponse(message="Course delete")