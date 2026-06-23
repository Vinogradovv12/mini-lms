from app.exceptions.base import DomainError


class LessonNotFoundError(
    DomainError
):
    code = "lesson_not_found"

    def __init__(self):
        super().__init__(
            "Lesson not found"
        )