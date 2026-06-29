from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.exceptions import raise_bad_request, raise_not_found

router = APIRouter(prefix="/users", tags=["Users"])

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Create User
@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    # Check duplicate email
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise_bad_request("Email already registered")

    user = User(
        name=payload.name,
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ✅ Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise_not_found("User")
    
    return user