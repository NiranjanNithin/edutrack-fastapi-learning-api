from sqlalchemy.orm import Session
from app.models.achievement import Achievement
from app.models.enrollment import Enrollment


def trigger_achievements(db: Session, user_id: int, total_lessons: int):

    # ✅ Count completed courses
    completed_courses = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.status == "completed"
    ).count()

    # ✅ Fast Starter → first course completion
    if completed_courses == 1:
        db.add(Achievement(user_id=user_id, title="Fast Starter"))

    # ✅ Deep Diver → course >=10 lessons
    if total_lessons >= 10:
        db.add(Achievement(user_id=user_id, title="Deep Diver"))

    db.commit()