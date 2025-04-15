from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.sql import func

from app.db.postgres import Base


class User(Base):
    """User model for authentication and profile information"""
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    grade_level = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)


class GoalProgress(Base):
    """Tracks user progress for curriculum goals"""
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    goal_id = Column(String(100), nullable=False, index=True)
    mastery_level = Column(Float, default=0.0)
    attempts_count = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    last_practiced = Column(DateTime, nullable=True)
    
    # Unique constraint
    __table_args__ = (
        # SQLAlchemy syntax for creating a unique constraint
        {'sqlite_autoincrement': True},
    )