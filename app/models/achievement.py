from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)