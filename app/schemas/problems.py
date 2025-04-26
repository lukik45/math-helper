from typing import List, Optional
from pydantic import BaseModel


class Goal(BaseModel):
    id: str
    description: str


class Requirement(BaseModel):
    id: str
    description: str


class CurriculumGoal(BaseModel):
    id: str
    description: str
    requirements: List[Requirement] = []


class SolutionStep(BaseModel):
    id: str
    step_number: int
    description: str
    hint: str
    solution: str
    curriculum_goals: List[CurriculumGoal] = []
    user_solved: bool = False
    solved_with_hint: Optional[bool] = None


class ProblemBase(BaseModel):
    problem_text: str
    subject_area: Optional[str] = None
    grade_level: Optional[int] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemResponse(ProblemBase):
    problem_id: str
    solution_steps: List[SolutionStep] = []


class StepProgressUpdate(BaseModel):
    solved_with_hint: bool