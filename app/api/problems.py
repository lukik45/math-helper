import uuid
import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from neo4j import Driver

from app.core.security import get_current_user
from app.db.base import get_db
from app.db.neo4j import get_neo4j
from app.models.users import User
from app.schemas.problems import ProblemCreate, ProblemResponse, StepProgressUpdate
from app.services.openai_integration import generate_solution
from app.services.curriculum_matching import match_step_to_curriculum
from app.services.progress_tracking import update_step_progress

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/solve", response_model=ProblemResponse)
def solve_problem(
    problem_in: ProblemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Solve a math problem and link to curriculum goals.
    """
    logger.info(f"User {current_user.id} requested solution for problem: {problem_in.problem_text}")
    
    # Generate solution using OpenAI
    solution_steps = generate_solution(
        problem_in.problem_text,
        problem_in.grade_level or current_user.grade_level
    )
    
    if not solution_steps:
        logger.error(f"Failed to generate solution for problem: {problem_in.problem_text}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate solution. Please check the OpenAI API key and try again."
        )
    
    logger.info(f"Generated {len(solution_steps)} solution steps")
    
    try:
        # Create problem ID
        problem_id = str(uuid.uuid4())
        logger.info(f"Created problem ID: {problem_id}")
        
        # Store problem in Neo4j
        with neo4j_driver.session() as session:
            session.run("""
                CREATE (p:Problem {
                    id: $id,
                    text: $text,
                    subject_area: $subject,
                    user_id: $user_id,
                    created_at: datetime()
                })
            """, id=problem_id, text=problem_in.problem_text, 
                 subject=problem_in.subject_area, user_id=current_user.id)
            
            logger.info(f"Stored problem in Neo4j")
            
            # Process each step
            for step in solution_steps:
                step_id = str(uuid.uuid4())
                step["id"] = step_id
                
                # Create step node
                session.run("""
                    MATCH (p:Problem {id: $problem_id})
                    CREATE (s:SolutionStep {
                        id: $id,
                        step_number: $num,
                        description: $desc,
                        hint: $hint,
                        solution: $solution,
                        user_solved: false,
                        solved_with_hint: null
                    })
                    CREATE (p)-[:HAS_STEP]->(s)
                """, problem_id=problem_id, id=step_id, num=step["step_number"], 
                     desc=step["description"], hint=step["hint"], 
                     solution=step["solution"])
                
                logger.info(f"Created step {step['step_number']} with ID {step_id}")
                
                # Match step to curriculum goals
                try:
                    curriculum_goals = match_step_to_curriculum(
                        step["description"], 
                        step["solution"],
                        neo4j_driver
                    )
                    
                    logger.info(f"Matched step to {len(curriculum_goals)} curriculum goals")
                    
                    # Store relationship between step and goals
                    for goal in curriculum_goals:
                        session.run("""
                            MATCH (s:SolutionStep {id: $step_id})
                            MERGE (g:Goal {id: $goal_id, description: $goal_desc})
                            CREATE (s)-[:RELATED_TO_GOAL]->(g)
                        """, step_id=step_id, goal_id=goal["id"], goal_desc=goal["description"])
                    
                    # Add curriculum goals to step response
                    step["curriculum_goals"] = curriculum_goals
                except Exception as e:
                    logger.error(f"Error matching step to curriculum: {str(e)}")
                    # Still continue even if curriculum matching fails
                    step["curriculum_goals"] = []
        
        # Create user-problem relationship
        with neo4j_driver.session() as session:
            session.run("""
                MATCH (p:Problem {id: $problem_id})
                MERGE (u:User {id: $user_id})
                CREATE (u)-[:ATTEMPTED]->(p)
            """, problem_id=problem_id, user_id=current_user.id)
            
            logger.info(f"Created user-problem relationship")
        
        # Return problem with steps
        logger.info(f"Returning solution with {len(solution_steps)} steps")
        return {
            "problem_id": problem_id,
            "problem_text": problem_in.problem_text,
            "subject_area": problem_in.subject_area,
            "grade_level": problem_in.grade_level,
            "solution_steps": solution_steps
        }
    except Exception as e:
        logger.error(f"Error in solve_problem: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the solution: {str(e)}"
        )

@router.get("/{problem_id}", response_model=ProblemResponse)
def get_problem(
    problem_id: str,
    current_user: User = Depends(get_current_user),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Get a problem by ID.
    """
    logger.info(f"User {current_user.id} requested problem {problem_id}")
    
    with neo4j_driver.session() as session:
        # Get problem
        problem_result = session.run("""
            MATCH (p:Problem {id: $problem_id})
            RETURN p.id as id, p.text as text, p.subject_area as subject_area
        """, problem_id=problem_id)
        
        problem_record = problem_result.single()
        if not problem_record:
            logger.warning(f"Problem {problem_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )
        
        problem = dict(problem_record)
        logger.info(f"Found problem: {problem['text'][:50]}...")
        
        # Get steps
        steps_result = session.run("""
            MATCH (p:Problem {id: $problem_id})-[:HAS_STEP]->(s:SolutionStep)
            RETURN s.id as id, s.step_number as step_number, s.description as description,
                   s.hint as hint, s.solution as solution, s.user_solved as user_solved,
                   s.solved_with_hint as solved_with_hint
            ORDER BY s.step_number
        """, problem_id=problem_id)
        
        steps = []
        for step_record in steps_result:
            step = dict(step_record)
            
            # Get curriculum goals for step
            goals_result = session.run("""
                MATCH (s:SolutionStep {id: $step_id})-[:RELATED_TO_GOAL]->(g:Goal)
                RETURN g.id as id, g.description as description
            """, step_id=step["id"])
            
            curriculum_goals = []
            for goal_record in goals_result:
                goal = dict(goal_record)
                
                # Get requirements for goal
                requirements_result = session.run("""
                    MATCH (g:Goal {id: $goal_id})<-[:HAS_GOAL]-(r:Requirement)
                    RETURN r.id as id, r.description as description
                """, goal_id=goal["id"])
                
                requirements = [dict(req) for req in requirements_result]
                
                curriculum_goals.append({
                    "id": goal["id"],
                    "description": goal["description"],
                    "requirements": requirements
                })
            
            step["curriculum_goals"] = curriculum_goals
            steps.append(step)
        
        logger.info(f"Found {len(steps)} steps for problem {problem_id}")
    
    return {
        "problem_id": problem["id"],
        "problem_text": problem["text"],
        "subject_area": problem["subject_area"],
        "grade_level": None,  # Not stored in Neo4j in this implementation
        "solution_steps": steps
    }

@router.post("/{problem_id}/steps/{step_id}/progress")
def update_step_progress_endpoint(
    problem_id: str,
    step_id: str,
    progress_update: StepProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    neo4j_driver: Driver = Depends(get_neo4j)
) -> Any:
    """
    Update user progress on a solution step.
    """
    logger.info(f"User {current_user.id} updating progress for step {step_id} of problem {problem_id}")
    
    result = update_step_progress(
        db=db,
        user_id=current_user.id,
        step_id=step_id,
        solved_with_hint=progress_update.solved_with_hint,
        neo4j_driver=neo4j_driver
    )
    
    logger.info(f"Progress updated: {result}")
    return result