from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from datetime import datetime
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.core.exceptions import raise_bad_request, raise_not_found
from app.services.achievement import trigger_achievements

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Create Enrollment
@router.post("/", response_model=EnrollmentResponse)
def enroll_user(payload: EnrollmentCreate, db: Session = Depends(get_db)):

    # ✅ Validate user exists
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise_not_found("User")

    # ✅ Validate course exists
    course = db.query(Course).filter(Course.id == payload.course_id).first()
    if not course:
        raise_not_found("Course")

    # ✅ Prevent duplicate active enrollment
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == payload.user_id,
        Enrollment.course_id == payload.course_id,
        Enrollment.status == "active"
    ).first()

    if existing:
        raise_bad_request("User already enrolled in this course")

    # ✅ Create enrollment
    enrollment = Enrollment(
        user_id=payload.user_id,
        course_id=payload.course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@router.post("/{enrollment_id}/complete-lesson")
def complete_lesson(enrollment_id: int, db: Session = Depends(get_db)):

    # ✅ Fetch enrollment
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    if not enrollment:
        raise_not_found("Enrollment")

    # ✅ Fetch course
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()

    if not course:
        raise_not_found("Course")

    # ✅ Prevent over-completion
    if enrollment.status == "completed":
        raise_bad_request("Course already completed")

    # ✅ Increment lesson
    enrollment.completed_lessons_count += 1

    # ✅ Completion logic
    if enrollment.completed_lessons_count >= course.total_lessons:
        enrollment.status = "completed"
        enrollment.completed_at = datetime.utcnow()

        db.commit()

        # ✅ Trigger achievements AFTER completion
        trigger_achievements(
            db,
            user_id=enrollment.user_id,
            total_lessons=course.total_lessons
        )

        return {"message": "Course completed 🎉"}

    db.commit()

    return {
        "message": "Lesson completed",
        "progress": f"{enrollment.completed_lessons_count}/{course.total_lessons}"
    }
