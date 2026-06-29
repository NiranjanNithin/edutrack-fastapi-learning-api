from pydantic import BaseModel, Field

# ✅ Request Schema
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str | None = Field(default=None, max_length=255)
    total_lessons: int = Field(..., gt=0, le=1000)  # must be >0


# ✅ Response Schema
class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    total_lessons: int

    class Config:
        from_attributes = True