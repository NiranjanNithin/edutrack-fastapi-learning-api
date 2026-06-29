from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.core.exceptions import raise_not_found

router = APIRouter(prefix="/courses", tags=["Courses"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Create Course
@router.post("/", response_model=CourseResponse)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):

    course = Course(
        title=payload.title,
        description=payload.description,
        total_lessons=payload.total_lessons
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


# ✅ Get Course by ID
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise_not_found("Course")

    return course


# ✅ Get All Courses
@router.get("/", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):

    courses = db.query(Course).all()
    return courses