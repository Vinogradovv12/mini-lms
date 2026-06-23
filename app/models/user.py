from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")

    authored_courses = relationship(
        "Course",
        back_populates="author"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="user"
    )

    @property
    def is_admin(self):
        return self.role.name == "admin"
    
    @property
    def is_author(self):
        return self.role.name == "author"
    
