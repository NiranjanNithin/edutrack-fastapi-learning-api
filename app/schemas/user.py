from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# ✅ Request Schema
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr   # automatic email validation


# ✅ Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # for SQLAlchemy compatibility
