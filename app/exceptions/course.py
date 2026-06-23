from app.exceptions.base import DomainError


class CourseNotFoundError(
    DomainError
):
    code = "course_not_found"

    def __init__(self):
        super().__init__(
            "Course not found"
        )


class AccessDeniedError(
    DomainError
):
    code = "access_denied"

    def __init__(self):
        super().__init__(
            "Access denied"
        )


class CourseAlreadyEnrolledError(
    DomainError
):
    code = "course_already_enrolled"

    def __init__(self):
        super().__init__(
            "Already enrolled"
        )