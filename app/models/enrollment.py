from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    completed_lessons_count = Column(Integer, default=0)
    status = Column(String, default="active")  # active / completed

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # ✅ Relationships (important!)
    user = relationship("User", backref="enrollments")
    course = relationship("Course", backref="enrollments")
