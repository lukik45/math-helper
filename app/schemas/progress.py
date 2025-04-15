from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GoalProgressBase(BaseModel):
    """Base schema for goal progress"""
    goal_id: str
    mastery_level: float = Field(0.0, ge=0.0, le=1.0)
    attempts_count: int = 0
    successful_attempts: int = 0
    last_practiced: Optional[datetime] = None


class GoalProgressCreate(GoalProgressBase):
    """Schema for creating goal progress"""
    user_id: int


class GoalProgressUpdate(BaseModel):
    """Schema for updating goal progress"""
    mastery_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    attempts_count: Optional[int] = None
    successful_attempts: Optional[int] = None
    last_practiced: Optional[datetime] = None


class GoalProgressResponse(GoalProgressBase):
    """Schema for goal progress response"""
    id: int
    user_id: int
    goal_description: Optional[str] = None

    class Config:
        from_attributes = True


class StepProgressUpdate(BaseModel):
    """Schema for updating step progress"""
    solved_with_hint: bool


class UserProgressSummary(BaseModel):
    """Schema for user progress summary"""
    total_problems_attempted: int
    problems_completed: int
    average_mastery: float
    struggling_areas: List[str]
    strongest_areas: List[str]
    recent_activity: List[dict]


class GoalProgressWithDetails(GoalProgressBase):
    """Schema for goal progress with additional details"""
    id: int
    user_id: int
    goal_description: str
    requirement_description: str
    chapter_name: str
    related_problems: List[dict] = []

    class Config:
        from_attributes = True


class UserSettingsBase(BaseModel):
    """Base schema for user settings"""
    difficulty_preference: str = "adaptive"  # adaptive, easy, medium, hard
    hint_preference: bool = True
    notification_enabled: bool = True
    theme: str = "light"


class UserSettingsUpdate(UserSettingsBase):
    """Schema for updating user settings"""
    pass


class UserSettingsResponse(UserSettingsBase):
    """Schema for user settings response"""
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True