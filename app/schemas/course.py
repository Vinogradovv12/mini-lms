from typing import List

from pydantic import BaseModel

from app.schemas.user import UserResponse


class CourseCreate(BaseModel):
    title: str
    description: str


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    
    author: UserResponse

    class Config:
        from_attributes = True


class UserCourseSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class UserCoursesResponse(BaseModel):
    id: int
    username: str
    courses: List[UserCourseSchema]
    
    class Config:
        from_attributes = True


class DashboardCoursesResponse(BaseModel):
    user_courses: List[CourseResponse]
    other_courses: List[CourseResponse]
