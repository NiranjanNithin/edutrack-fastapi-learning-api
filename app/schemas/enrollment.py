from pydantic import BaseModel, Field
from datetime import datetime


# ✅ Request Schema
class EnrollmentCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    course_id: int = Field(..., gt=0)


# ✅ Response Schema
class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    completed_lessons_count: int
    status: str
    started_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True