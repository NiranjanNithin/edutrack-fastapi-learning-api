from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.user import User
from app.models.enrollment import Enrollment

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):

    leaderboard = (
        db.query(
            User.id,
            User.name,
            func.sum(Enrollment.completed_lessons_count).label("total_lessons_completed")
        )
        .join(Enrollment, User.id == Enrollment.user_id)
        .group_by(User.id)
        .order_by(func.sum(Enrollment.completed_lessons_count).desc())
        .limit(5)
        .all()
    )

    result = []

    for row in leaderboard:
        result.append({
            "user_id": row.id,
            "name": row.name,
            "total_lessons_completed": row.total_lessons_completed
        })

    return result