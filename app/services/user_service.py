from sqlalchemy import func
from sqlalchemy.orm import Session

from app.exceptions.auth import UserAlreadyExistsError
from app.exceptions.user import RoleNotFoundError, UserNotFoundError
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate

from app.services.course_service import get_user_courses
from app.core.security import hash_password


def create_user(
    db: Session,
    user: UserCreate
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise UserAlreadyExistsError()

    role = db.query(Role).filter(
        Role.id == user.role_id
    ).first()

    if not role:
        raise RoleNotFoundError()
    

    hashed_password = hash_password(
        user.password
    )

    db_user = User(
        username = user.username,
        email = user.email,
        password_hash = hashed_password,
        role_id = user.role_id
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_user_by_id(
    db: Session,
    user_id: int
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:
        raise UserNotFoundError()
    
    return user


def get_all_users(
    db: Session
):
    return db.query(User).all()


def get_user_with_courses(
    db: Session,
    user_id: int
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise UserNotFoundError()

    return {
        "id": user.id,
        "username": user.username,
        "courses": get_user_courses(
            db,
            user_id
        )
    }


def get_users_data(
    db: Session
):

    results = (
        db.query(
            User,

            func.count(
                func.distinct(
                    Course.id
                )
            ).label(
                "created_count"
            ),

            func.count(
                func.distinct(
                    Enrollment.id
                )
            ).label(
                "enrolled_count"
            )

        )
        .outerjoin(
            User.authored_courses
        )
        .outerjoin(
            User.enrollments
        )
        .group_by(
            User.id
        )
        .all()
    )

    return [
        {
            "user": user,
            "created": created,
            "enrolled": enrolled
        }

        for user,
        created,
        enrolled in results
    ]
        