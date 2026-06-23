from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.enrollment import EnrollmentResponse

from app.dependencies.api.auth import get_current_actor
from app.services.enrollment_service import enroll_user


router = APIRouter(
    prefix="/api/enrollments",
    tags=["Enrollments"]
)


@router.post("/{course_id}", response_model=EnrollmentResponse)
def enroll_user_endpoint(
    course_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_actor)
):
    return enroll_user(
        db,
        course_id=course_id,
        actor=current_user
    )

    