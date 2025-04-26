from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from neo4j import GraphDatabase

from app.models.users import GoalProgress
from app.db.neo4j import get_neo4j

def update_step_progress(
    db: Session, 
    user_id: int, 
    step_id: str, 
    solved_with_hint: bool,
    neo4j_driver=None
) -> Dict[str, Any]:
    """Update user progress for a solution step"""
    if neo4j_driver is None:
        neo4j_driver = get_neo4j()
    
    # Update the step status in Neo4j
    with neo4j_driver.session() as session:
        # First check if the step exists
        step_check = session.run("""
            MATCH (s:SolutionStep {id: $step_id})
            RETURN s
        """, step_id=step_id)
        
        if not step_check.single():
            # For MVP, create the step if it doesn't exist
            session.run("""
                CREATE (s:SolutionStep {
                    id: $step_id,
                    user_solved: true,
                    solved_with_hint: $solved_with_hint
                })
            """, step_id=step_id, solved_with_hint=solved_with_hint)
        else:
            # Update the existing step
            session.run("""
                MATCH (s:SolutionStep {id: $step_id})
                SET s.user_solved = true,
                    s.solved_with_hint = $solved_with_hint
            """, step_id=step_id, solved_with_hint=solved_with_hint)
        
        # Get related goals (for MVP, we'll use sample data if none exist)
        result = session.run("""
            MATCH (s:SolutionStep {id: $step_id})-[:RELATED_TO_GOAL]->(g:Goal)
            RETURN g.id as id, g.description as description
        """, step_id=step_id)
        
        goals = [dict(record) for record in result]
        
        # For MVP, provide sample goals if none exist
        if not goals:
            goals = [
                {"id": "sample_goal_1", "description": "Use algebraic methods to solve equations"},
                {"id": "sample_goal_2", "description": "Apply mathematical knowledge to real-world problems"}
            ]
    
    # Update goal mastery in SQLite
    for goal in goals:
        # Check if goal progress exists
        progress = db.query(GoalProgress).filter(
            GoalProgress.user_id == user_id,
            GoalProgress.goal_id == goal["id"]
        ).first()
        
        if progress:
            # Update existing progress
            progress.attempts_count += 1
            if not solved_with_hint:
                progress.successful_attempts += 1
            else:
                # For hint-based solutions, we count it as 0.5 success
                progress.successful_attempts += 0.5
            
            # Recalculate mastery level
            progress.mastery_level = min(1.0, progress.successful_attempts / progress.attempts_count)
            progress.last_practiced = datetime.utcnow()
        else:
            # Create new goal progress
            mastery = 0.5 if solved_with_hint else 1.0
            new_progress = GoalProgress(
                user_id=user_id,
                goal_id=goal["id"],
                mastery_level=mastery,
                attempts_count=1,
                successful_attempts=0.5 if solved_with_hint else 1.0,
                last_practiced=datetime.utcnow()
            )
            db.add(new_progress)
        
        db.commit()
    
    return {"success": True, "updated_goals": len(goals)}