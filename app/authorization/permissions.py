from sqlalchemy import exists

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User

def is_course_author(user: User, course: Course) -> bool:
    return user and course and course.author_id == user.id


def is_enrolled(db, user: User, course: Course) -> bool:
    return db.query(
        exists().where(
            Enrollment.user_id == user.id,
            Enrollment.course_id == course.id
        )
    ).scalar()


def can_create_course(user: User) -> bool:
    return user and (user.is_admin or user.is_author)


def can_access_course(db, user: User, course: Course) -> bool:
    return (
        user and (
            user.is_admin 
            or is_course_author(user, course)
            or is_enrolled(db, user, course)
        )
    )


def can_manage_course(user: User, course: Course) -> bool:
    if not user or not course:
        return False
    
    return user.is_admin or is_course_author(user, course)
