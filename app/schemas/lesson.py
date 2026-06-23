from pydantic import BaseModel

class LessonCreate(BaseModel):
    title: str
    content: str
    description: str
    

class LessonResponse(BaseModel):
    id: int
    title: str
    description: str
    content: str
    course_id: int

    class Config:
        from_attributes = True


class LessonPreviewResponse(BaseModel):
    id: int
    title: str
    description: str
    course_id: int
        