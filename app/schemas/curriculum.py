from typing import List, Optional

from pydantic import BaseModel


class ChapterBase(BaseModel):
    """Base schema for curriculum chapters"""
    id: str
    name: str
    grade_level: int


class RequirementBase(BaseModel):
    """Base schema for curriculum requirements"""
    id: str
    description: str


class GoalBase(BaseModel):
    """Base schema for curriculum goals"""
    id: str
    description: str


class RequirementWithGoals(RequirementBase):
    """Schema for requirements with associated goals"""
    goals: List[GoalBase] = []


class ChapterWithRequirements(ChapterBase):
    """Schema for chapters with associated requirements"""
    requirements: List[RequirementBase] = []


class ChapterDetail(ChapterBase):
    """Detailed schema for chapters with requirements and goals"""
    requirements: List[RequirementWithGoals] = []


class CurriculumStructure(BaseModel):
    """Schema for full curriculum structure"""
    chapters: List[ChapterDetail] = []


class GoalWithRequirements(GoalBase):
    """Schema for goals with parent requirements"""
    requirement: RequirementBase
    chapter: ChapterBase


class GoalWithProgress(GoalBase):
    """Schema for goals with user progress"""
    mastery_level: float = 0.0
    attempts_count: int = 0
    last_practiced: Optional[str] = None