from sqlalchemy import Column, Integer, ForeignKey, DateTime

from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    user = relationship(
        "User",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )