from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field


class GoalBase(BaseModel):
    """Base schema for curriculum goals"""
    id: str
    description: str


class RequirementBase(BaseModel):
    """Base schema for curriculum requirements"""
    id: str
    description: str


class CurriculumGoal(GoalBase):
    """Schema for curriculum goals with related requirements"""
    requirements: List[RequirementBase] = []


class SolutionStepBase(BaseModel):
    """Base schema for solution steps"""
    description: str
    hint: str
    solution: str


class SolutionStepCreate(SolutionStepBase):
    """Schema for creating a solution step"""
    step_number: int


class SolutionStepUpdate(BaseModel):
    """Schema for updating a solution step"""
    user_solved: Optional[bool] = None
    solved_with_hint: Optional[bool] = None


class SolutionStep(SolutionStepBase):
    """Full schema for a solution step including ID and status"""
    id: str
    step_number: int
    user_solved: bool = False
    solved_with_hint: Optional[bool] = None
    curriculum_goals: List[CurriculumGoal] = []


class ProblemBase(BaseModel):
    """Base schema for math problems"""
    text: str
    subject_area: str = Field(..., min_length=1, max_length=100)
    difficulty: int = Field(1, ge=1, le=5)


class ProblemCreate(ProblemBase):
    """Schema for creating a new problem"""
    grade_level: Optional[int] = Field(None, ge=1, le=12)


class ProblemSolveRequest(BaseModel):
    """Schema for problem solution request"""
    problem_text: str = Field(..., min_length=1)
    subject_area: Optional[str] = None
    grade_level: Optional[int] = Field(None, ge=1, le=12)


class ProblemSolution(BaseModel):
    """Schema for problem solution response"""
    problem_id: str
    problem_text: str
    subject_area: Optional[str] = None
    solution_steps: List[SolutionStep]


class ProblemResponse(ProblemBase):
    """Schema for problem response"""
    id: str
    created_at: datetime
    user_id: Optional[int] = None
    solution_steps: Optional[List[SolutionStep]] = None


class ProblemHistoryResponse(BaseModel):
    """Schema for problem history response"""
    problem_id: str
    problem_text: str
    subject_area: str
    attempted_at: datetime
    completed: bool
    time_spent_seconds: Optional[int] = None
    steps_completed: int
    steps_with_hints: int


class ProblemRecommendation(BaseModel):
    """Schema for problem recommendation"""
    problem_id: str
    problem_text: str
    subject_area: str
    difficulty: int
    related_goals: List[GoalBase]
    recommendation_reason: str