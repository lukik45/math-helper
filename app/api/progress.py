from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from neo4j import Driver

from app.core.security import get_current_user
from app.db.base import get_db
from app.db.neo4j import get_neo4j
from app.models.users import User, GoalProgress
from app.schemas.progress import UserProgressStats, GoalProgressResponse

router = APIRouter()

@router.get("/{user_id}", response_model=UserProgressStats)
def get_user_progress(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get user's learning progress statistics.
    """
    # Check if user is fetching their own progress
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this user's progress"
        )
    
    # Get all goal progress records
    progress_records = db.query(GoalProgress).filter(
        GoalProgress.user_id == user_id
    ).all()
    
    # Calculate stats
    total_goals = len(progress_records)
    mastered_goals = sum(1 for p in progress_records if p.mastery_level >= 0.8)
    struggling_goals = sum(1 for p in progress_records if p.mastery_level < 0.5)
    
    average_mastery = 0
    if total_goals > 0:
        average_mastery = sum(p.mastery_level for p in progress_records) / total_goals
    
    # Get goal descriptions from Neo4j
    goal_descriptions = {}
    if progress_records:
        goal_ids = [p.goal_id for p in progress_records]
        
        with neo4j_driver.session() as session:
            result = session.run("""
                MATCH (g:Goal)
                WHERE g.id IN $goal_ids
                RETURN g.id as id, g.description as description
            """, goal_ids=goal_ids)
            
            for record in result:
                goal_descriptions[record["id"]] = record["description"]
    
    # Create response objects
    goal_progress_response = []
    for progress in progress_records:
        description = goal_descriptions.get(progress.goal_id, "Unknown Goal")
        goal_progress_response.append({
            "id": progress.id,
            "user_id": progress.user_id,
            "goal_id": progress.goal_id,
            "goal_description": description,
            "mastery_level": progress.mastery_level,
            "attempts_count": progress.attempts_count,
            "successful_attempts": progress.successful_attempts,
            "last_practiced": progress.last_practiced
        })
    
    return {
        "total_goals": total_goals,
        "mastered_goals": mastered_goals,
        "struggling_goals": struggling_goals,
        "average_mastery": average_mastery,
        "goal_progress": goal_progress_response
    }

@router.get("/recommend/{user_id}", response_model=List[dict])
def get_recommended_problems(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get problems recommended based on user's struggling goals.
    """
    # Check if user is fetching their own recommendations
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this user's recommendations"
        )
    
    # Get struggling goals
    struggling_goals = db.query(GoalProgress).filter(
        GoalProgress.user_id == user_id,
        GoalProgress.mastery_level < 0.6
    ).order_by(GoalProgress.mastery_level.asc()).limit(5).all()
    
    if not struggling_goals:
        return []
    
    # Get goal IDs
    goal_ids = [goal.goal_id for goal in struggling_goals]
    
    # Find problems targeting these goals
    with neo4j_driver.session() as session:
        # Try to find problems related to the struggling goals
        result = session.run("""
            MATCH (g:Goal)<-[:RELATED_TO_GOAL]-(s:SolutionStep)<-[:HAS_STEP]-(p:Problem)
            WHERE g.id IN $goal_ids
            AND NOT EXISTS {
                MATCH (u:User {id: $user_id})-[:ATTEMPTED]->(p)
            }
            RETURN DISTINCT p.id as id, p.text as text, 
                   p.subject_area as subject_area,
                   collect(DISTINCT g.id) as goal_ids,
                   collect(DISTINCT g.description) as goal_descriptions
            LIMIT 5
        """, goal_ids=goal_ids, user_id=user_id)
        
        recommended_problems = [dict(record) for record in result]
        
        # If no problems found, return sample problems for MVP
        if not recommended_problems:
            return [
                {
                    "id": "sample_problem_1",
                    "text": "Solve the equation: 2x + 5 = 13",
                    "subject_area": "Algebra",
                    "goal_ids": [goal_ids[0]],
                    "goal_descriptions": ["Use algebraic methods to solve equations"]
                },
                {
                    "id": "sample_problem_2",
                    "text": "Calculate the area of a circle with radius 5 cm",
                    "subject_area": "Geometry",
                    "goal_ids": [goal_ids[0]],
                    "goal_descriptions": ["Apply mathematical knowledge to real-world problems"]
                }
            ]
        
        return recommended_problems