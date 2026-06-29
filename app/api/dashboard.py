from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.achievement import Achievement
from app.core.exceptions import raise_not_found

router = APIRouter(prefix="/users", tags=["Dashboard"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}/dashboard")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):

    # ✅ Get User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise_not_found("User")

    # ✅ Active Enrollments
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.status == "active"
    ).all()

    active_courses = []

    for e in enrollments:
        course = db.query(Course).filter(Course.id == e.course_id).first()

        progress = (e.completed_lessons_count / course.total_lessons) * 100

        active_courses.append({
            "course_id": course.id,
            "title": course.title,
            "progress_percentage": round(progress, 2)
        })

    # ✅ Achievements
    achievements = db.query(Achievement).filter(
        Achievement.user_id == user_id
    ).all()

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "active_courses": active_courses,
        "achievements": [a.title for a in achievements]
    }