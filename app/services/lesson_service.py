from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload

from app.exceptions.course import AccessDeniedError, CourseNotFoundError
from app.exceptions.lesson import LessonNotFoundError
from app.models.lesson import Lesson

from app.services.course_service import get_course
from app.authorization.permissions import can_manage_course, is_enrolled

from app.core.logger import logger

def create_lesson(
    db: Session,
    actor,
    course_id: int,
    title: str,
    description: str,
    content: str
):
    course = get_course(
        db,
        course_id
    )

    if not course:
        raise CourseNotFoundError()

    if not can_manage_course(
        actor,
        course
    ):
        logger.warning(
            f"ACCESS_DENIED | "
            f"user={actor.id} | "
            f"action=create_lesson | "
            f"course_id={course_id}"
        )
        
        raise AccessDeniedError()

    lesson = Lesson(
        title=title,
        content=content,
        description=description,
        course_id=course_id
    )

    db.add(lesson)

    db.commit()

    db.refresh(lesson)

    logger.info(
        f"LESSON_CREATED | "
        f"user={actor.id} | "
        f"course_id={course_id} | "
        f"lesson_id={lesson.id}"
    )

    return lesson


def get_lesson_by_id(
    db: Session,
    lesson_id: int,
    actor
):
    lesson = db.query(Lesson).options(
        joinedload(Lesson.course)
    ).filter(
        Lesson.id == lesson_id
    ).first()

    if not lesson:
        raise LessonNotFoundError()
    
    if not(
        is_enrolled(
            db,
            actor,
            lesson.course
        )
        or can_manage_course(
            actor,
            lesson.course
        )
    ):
        raise AccessDeniedError()

    
    return lesson

def get_lessons_by_course_id(
    db: Session,
    course_id: int
):
    course = get_course(
        db,
        course_id
    )

    if not course:
        raise CourseNotFoundError()

    lessons = course.lessons

    if not lessons:
        raise LessonNotFoundError()
    
    return lessons