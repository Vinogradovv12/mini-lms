from fastapi import HTTPException

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.exceptions.course import AccessDeniedError, CourseNotFoundError
from app.models.course import Course
from app.models.enrollment import Enrollment

from app.authorization.permissions import can_create_course, can_manage_course

from app.core.logger import logger
from app.schemas.course import DashboardCoursesResponse

def create_course(
    db: Session,
    title: str,
    description: str,
    actor
):
    if not can_create_course(
        actor
    ):
        raise AccessDeniedError()

    course = Course(
        title=title,
        description=description,
        author_id=actor.id
    )

    db.add(course)

    db.commit() 

    db.refresh(course)

    logger.info(
        f"COURSE_CREATED | "
        f"course_id={course.id} | "
    )

    return course


def get_course(
    db: Session,
    course_id: int
):
    course = (
        db.query(Course)
        .options(
            joinedload(Course.author),
            joinedload(Course.lessons)
        )
        .filter(
            Course.id == course_id
        )
        .first()
    )

    if not course:
        raise CourseNotFoundError()
    
    return course

def list_public_courses(
    db: Session,
):
    return db.query(Course).all()


def update_course(
    db: Session,
    course_id: int,
    title: str,
    description: str,
    actor
):
    course = get_course(
        db,
        course_id
    )
    
    if not can_manage_course(
        actor,
        course
    ):
        logger.warning(
            f"ACCESS_DENIED | "
            f"email={actor.email} | "
            f"path=update_course | "
            f"course_id={course_id} | "
        )

        raise AccessDeniedError()
    
    
    course.title = title
    course.description = description

    db.commit()

    db.refresh(course)

    logger.info(
        f"COURSE_UPDATED | "
        f"actor={actor.email} | "
        f"course_id={course.id}"
    )

    return course


def delete_course(
    db: Session,
    course_id: int,
    actor
):
    course = get_course(
        db,
        course_id
    )
    
    if not can_manage_course(
        actor,
        course
    ):
        logger.warning(
            f"ACCESS_DENIED | "
            f"email={actor.email} | "
            f"path=delete_course | "
            f"course_id={course_id} | "
        )

        raise AccessDeniedError()
    
    db.delete(course)

    db.commit()

    logger.warning(
        f"COURSE_DELETED | "
        f"actor={actor.email} | "
        f"course_id={course.id}"
    )


def get_user_courses(
    db: Session,
    user_id: int
):
    return (
        db.query(Course)
        .outerjoin(
            Enrollment,
            Course.id == Enrollment.course_id
        )
        .filter(
            or_(
                Course.author_id == user_id,
                Enrollment.user_id == user_id
            )
        )
        .distinct()
        .all()
    )


def get_other_courses(
    db: Session,
    user_id: int
):
    subquery = (
        db.query(Course.id)
        .outerjoin(
            Enrollment,
            Course.id == Enrollment.course_id
        )
        .filter(
            or_(
                Course.author_id == user_id,
                Enrollment.user_id == user_id
            )
        )
    )

    return (
        db.query(Course)
        .filter(
            ~Course.id.in_(subquery)
        )
        .all()
    )

def get_dashboard_courses(
    db: Session,
    user_id: int
):
    user_courses = get_user_courses(
        db,
        user_id
    )

    other_courses = get_other_courses(
        db,
        user_id
    )

    # return {
    #     "user_courses": user_courses,
    #     "other_courses": other_courses
    # }

    return DashboardCoursesResponse(
        user_courses=get_user_courses(
            db,
            user_id
        ),
        other_courses=get_other_courses(
            db,
            user_id
        )
    ).model_dump()