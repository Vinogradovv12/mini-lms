from pydantic import BaseModel

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User


class CourseAccess(BaseModel):
    actor: User
    course: Course

    class Config:
        arbitrary_types_allowed = True


class LessonAccess(BaseModel):
    actor: User
    lesson: Lesson

    class Config:
        arbitrary_types_allowed = True

        