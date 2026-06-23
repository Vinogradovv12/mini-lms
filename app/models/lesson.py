from sqlalchemy import Column, Integer, String, ForeignKey, Text

from sqlalchemy.orm import relationship

from app.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    content = Column(Text)

    description = Column(String)

    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship(
        "Course",
        back_populates="lessons"
    )