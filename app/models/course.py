from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    total_lessons = Column(Integer, nullable=False)