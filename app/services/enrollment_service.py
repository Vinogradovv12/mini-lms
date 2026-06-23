from app.core.logger import logger
from app.models.enrollment import Enrollment
from app.services.course_service import get_course
from app.authorization.permissions import is_enrolled

from app.exceptions.course import CourseAlreadyEnrolledError, CourseNotFoundError


def enroll_user(
    db,
    course_id: int,
    actor
):
    course = get_course(
        db,
        course_id=course_id
    )

    if not course:
        raise CourseNotFoundError()

    enroll_existing = is_enrolled(db, actor, course)

    if enroll_existing:
        raise CourseAlreadyEnrolledError()
    
    enrollment = Enrollment(
        user_id=actor.id,
        course_id=course.id
    )

    db.add(enrollment)

    db.commit()

    db.refresh(enrollment)

    logger.info(
        f"COURSE_ENROLLED | "
        f"email={actor.email} | "
        f"course_id={course_id} | "
    )

    return enrollment