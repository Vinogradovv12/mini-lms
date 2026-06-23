from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.database import get_db

from app.schemas.course import UserCoursesResponse
from app.schemas.user import UserCreate, UserResponse

from app.services.user_service import create_user, get_all_users, get_user_with_courses
from app.dependencies.api.auth import require_admin


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    return create_user(
        db,
        user
    )
        

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    return get_all_users(
        db
    )


@router.get("/{user_id}/courses", response_model=UserCoursesResponse)
def get_user_courses_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return get_user_with_courses(
        db,
        user_id
    )

