# Note: These are not SQLAlchemy models, but rather representations of Neo4j nodes
# They are used for type hinting and documentation purposes

from datetime import datetime
from typing import List, Optional, Dict, Any


class Problem:
    """
    Problem node in Neo4j
    
    This is a representation of the Problem node in Neo4j.
    """
    id: str
    text: str
    subject_area: str
    difficulty: int
    user_id: Optional[int]
    created_at: datetime
    
    def __init__(
        self,
        id: str,
        text: str,
        subject_area: str,
        difficulty: int = 1,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.text = text
        self.subject_area = subject_area
        self.difficulty = difficulty
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Problem":
        """Create a Problem instance from a dictionary"""
        return Problem(
            id=data.get("id"),
            text=data.get("text"),
            subject_area=data.get("subject_area"),
            difficulty=data.get("difficulty", 1),
            user_id=data.get("user_id"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Problem to a dictionary for Neo4j"""
        return {
            "id": self.id,
            "text": self.text,
            "subject_area": self.subject_area,
            "difficulty": self.difficulty,
            "user_id": self.user_id,
            "created_at": self.created_at
        }


class SolutionStep:
    """
    SolutionStep node in Neo4j
    
    This is a representation of the SolutionStep node in Neo4j.
    """
    id: str
    step_number: int
    description: str
    hint: str
    solution: str
    user_solved: bool
    solved_with_hint: Optional[bool]
    
    def __init__(
        self,
        id: str,
        step_number: int,
        description: str,
        hint: str,
        solution: str,
        user_solved: bool = False,
        solved_with_hint: Optional[bool] = None
    ):
        self.id = id
        self.step_number = step_number
        self.description = description
        self.hint = hint
        self.solution = solution
        self.user_solved = user_solved
        self.solved_with_hint = solved_with_hint
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "SolutionStep":
        """Create a SolutionStep instance from a dictionary"""
        return SolutionStep(
            id=data.get("id"),
            step_number=data.get("step_number"),
            description=data.get("description"),
            hint=data.get("hint"),
            solution=data.get("solution"),
            user_solved=data.get("user_solved", False),
            solved_with_hint=data.get("solved_with_hint")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert SolutionStep to a dictionary for Neo4j"""
        return {
            "id": self.id,
            "step_number": self.step_number,
            "description": self.description,
            "hint": self.hint,
            "solution": self.solution,
            "user_solved": self.user_solved,
            "solved_with_hint": self.solved_with_hint
        }