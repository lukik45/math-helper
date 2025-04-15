from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.db.postgres import Base


class User(Base):
    """User model for authentication and profile information"""
    
    __tablename__ = "users"
    
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
    
    __tablename__ = "goal_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(String(100), nullable=False, index=True)
    mastery_level = Column(Float, default=0.0)
    attempts_count = Column(Integer, default=0)
    successful_attempts = Column(Integer, default=0)
    last_practiced = Column(DateTime, nullable=True)
    
    # Unique constraint for user_id and goal_id
    __table_args__ = (
        UniqueConstraint('user_id', 'goal_id', name='uq_user_goal'),
    )


class ProblemHistory(Base):
    """Tracks problems attempted by users"""
    
    __tablename__ = "problem_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(String(100), nullable=False, index=True)
    attempted_at = Column(DateTime, server_default=func.now())
    completed = Column(Boolean, default=False)
    time_spent_seconds = Column(Integer, nullable=True)
    steps_completed = Column(Integer, default=0)
    steps_with_hints = Column(Integer, default=0)


class UserSettings(Base):
    """Stores user preferences"""
    
    __tablename__ = "user_settings"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    difficulty_preference = Column(String(20), default="adaptive")
    hint_preference = Column(Boolean, default=True)
    notification_enabled = Column(Boolean, default=True)
    theme = Column(String(20), default="light")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())