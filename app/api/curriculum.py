from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Driver

from app.core.security import get_current_user
from app.db.neo4j import get_neo4j
from app.models.users import User

router = APIRouter()

@router.get("/chapters")
def get_curriculum_chapters(
    current_user: User = Depends(get_current_user),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get all curriculum chapters.
    """
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (c:Chapter)
            RETURN c.id as id, c.name as name, c.grade_level as grade_level
            ORDER BY c.grade_level, c.name
        """)
        
        chapters = [dict(record) for record in result]
        
        # If no chapters found, return sample data for MVP
        if not chapters:
            return [
                {"id": "ch_1", "name": "Numbers and Calculations", "grade_level": 7},
                {"id": "ch_2", "name": "Algebra", "grade_level": 7},
                {"id": "ch_3", "name": "Geometry", "grade_level": 7},
                {"id": "ch_4", "name": "Statistics and Probability", "grade_level": 7}
            ]
        
        return chapters

@router.get("/requirements/{chapter_id}")
def get_chapter_requirements(
    chapter_id: str,
    current_user: User = Depends(get_current_user),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get requirements for a specific chapter.
    """
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (c:Chapter {id: $chapter_id})-[:HAS_REQUIREMENT]->(r:Requirement)
            RETURN r.id as id, r.description as description
            ORDER BY r.id
        """, chapter_id=chapter_id)
        
        requirements = [dict(record) for record in result]
        
        # If no requirements found, return sample data for MVP
        if not requirements:
            return [
                {"id": "req_1", "description": "Solve linear equations"},
                {"id": "req_2", "description": "Perform operations on algebraic expressions"},
                {"id": "req_3", "description": "Apply proportional reasoning"}
            ]
        
        return requirements

@router.get("/goals/{requirement_id}")
def get_requirement_goals(
    requirement_id: str,
    current_user: User = Depends(get_current_user),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get goals for a specific requirement.
    """
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (r:Requirement {id: $requirement_id})-[:HAS_GOAL]->(g:Goal)
            RETURN g.id as id, g.description as description
            ORDER BY g.id
        """, requirement_id=requirement_id)
        
        goals = [dict(record) for record in result]
        
        # If no goals found, return sample data for MVP
        if not goals:
            return [
                {"id": "goal_1", "description": "Use algebraic methods to solve linear equations"},
                {"id": "goal_2", "description": "Apply equation solving to real-world problems"},
                {"id": "goal_3", "description": "Verify solutions by substitution"}
            ]
        
        return goals