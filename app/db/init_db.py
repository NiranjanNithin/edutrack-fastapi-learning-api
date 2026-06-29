from sqlalchemy.orm import Session
from app.models.course import Course

def seed_courses(db: Session):

    existing = db.query(Course).count()
    if existing > 0:
        return

    courses = [
        Course(title="Python Basics", description="Learn Python", total_lessons=5),
        Course(title="Intro to FastAPI", description="Build APIs", total_lessons=3),
        Course(title="SQL 101", description="Database Fundamentals", total_lessons=10),
    ]

    db.add_all(courses)
    db.commit()