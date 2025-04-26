from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class GoalProgressBase(BaseModel):
    goal_id: str
    mastery_level: float
    attempts_count: int
    successful_attempts: int
    last_practiced: Optional[datetime] = None


class GoalProgressResponse(GoalProgressBase):
    id: int
    user_id: int
    goal_description: str

    class Config:
        orm_mode = True


class UserProgressStats(BaseModel):
    total_goals: int
    mastered_goals: int
    struggling_goals: int
    average_mastery: float
    goal_progress: List[GoalProgressResponse] = []