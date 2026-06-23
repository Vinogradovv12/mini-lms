from sqlalchemy import Column, Integer, String, ForeignKey, Text

from sqlalchemy.orm import relationship

from app.database import Base

class Course(Base):
    __tablename__ ="courses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text)

    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship(
        "User",
        back_populates="authored_courses"
    )

    lessons = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )