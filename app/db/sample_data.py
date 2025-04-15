import os
import uuid
from datetime import datetime, timedelta
from typing import List

from loguru import logger
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.neo4j import neo4j_db
from app.models.users import User, GoalProgress, ProblemHistory, UserSettings


def create_sample_users(db: Session) -> List[User]:
    """Create sample users for testing"""
    
    # Check if users already exist
    existing_users = db.query(User).count()
    if existing_users > 0:
        logger.info(f"Found {existing_users} existing users, skipping sample user creation")
        return db.query(User).all()
    
    # Create sample users
    sample_users = [
        User(
            username="student1",
            email="student1@example.com",
            hashed_password=get_password_hash("password123"),
            grade_level=8,
            created_at=datetime.now() - timedelta(days=30),
            last_login=datetime.now() - timedelta(days=2)
        ),
        User(
            username="student2",
            email="student2@example.com",
            hashed_password=get_password_hash("password123"),
            grade_level=9,
            created_at=datetime.now() - timedelta(days=25),
            last_login=datetime.now() - timedelta(days=1)
        ),
        User(
            username="teacher1",
            email="teacher1@example.com",
            hashed_password=get_password_hash("teacher123"),
            grade_level=None,
            created_at=datetime.now() - timedelta(days=60),
            last_login=datetime.now() - timedelta(hours=5)
        ),
    ]
    
    # Add to database
    for user in sample_users:
        db.add(user)
    
    db.commit()
    logger.info(f"Created {len(sample_users)} sample users")
    
    # Create user settings for each user
    for user in sample_users:
        db.add(UserSettings(user_id=user.id))
    
    db.commit()
    logger.info(f"Created user settings for sample users")
    
    return sample_users


def create_sample_goal_progress(db: Session, users: List[User]) -> None:
    """Create sample goal progress for testing"""
    
    # Check if goal progress already exists
    existing_progress = db.query(GoalProgress).count()
    if existing_progress > 0:
        logger.info(f"Found {existing_progress} existing goal progress entries, skipping sample creation")
        return
    
    # Get goals from Neo4j
    goals = neo4j_db.run_query("MATCH (g:Goal) RETURN g.id as id, g.description as description")
    if not goals:
        logger.warning("No goals found in Neo4j, cannot create sample goal progress")
        return
    
    # Create sample goal progress for each user
    goal_progress_entries = []
    
    for user in users:
        for goal in goals:
            # Random mastery level for testing
            import random
            mastery_level = round(random.uniform(0, 1.0), 2)
            attempts_count = random.randint(1, 10)
            successful_attempts = round(mastery_level * attempts_count)
            
            goal_progress_entries.append(
                GoalProgress(
                    user_id=user.id,
                    goal_id=goal["id"],
                    mastery_level=mastery_level,
                    attempts_count=attempts_count,
                    successful_attempts=successful_attempts,
                    last_practiced=datetime.now() - timedelta(days=random.randint(0, 14))
                )
            )
    
    # Add to database
    for progress in goal_progress_entries:
        db.add(progress)
    
    db.commit()
    logger.info(f"Created {len(goal_progress_entries)} sample goal progress entries")


def create_sample_problems(neo4j_instance) -> None:
    """Create sample problems in Neo4j for testing"""
    
    # Check if problems already exist
    problem_count = neo4j_instance.run_query_single(
        "MATCH (p:Problem) RETURN count(p) as count"
    )
    if problem_count and problem_count["count"] > 0:
        logger.info(f"Found {problem_count['count']} existing problems, skipping sample problem creation")
        return
    
    # Sample problems with solutions
    sample_problems = [
        {
            "id": str(uuid.uuid4()),
            "text": "Solve the equation: 2x + 5 = 15",
            "subject_area": "Algebra",
            "difficulty": 1,
            "user_id": None,
            "steps": [
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 1,
                    "description": "Subtract 5 from both sides of the equation",
                    "hint": "To isolate the variable term (2x), we need to move all other terms to the right side. What operation would cancel out +5 on the left side?",
                    "solution": "2x + 5 - 5 = 15 - 5\n2x = 10"
                },
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 2,
                    "description": "Divide both sides by 2",
                    "hint": "To isolate x, we need to divide both sides by the coefficient of x. What is the coefficient of x in this equation?",
                    "solution": "2x ÷ 2 = 10 ÷ 2\nx = 5"
                }
            ],
            "related_goals": ["G5", "G7"]  # IDs from curriculum setup
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Calculate the area of a circle with radius 4 cm",
            "subject_area": "Geometry",
            "difficulty": 2,
            "user_id": None,
            "steps": [
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 1,
                    "description": "Recall the formula for the area of a circle",
                    "hint": "The area of a circle is calculated using the radius. What is the formula that relates the area to the radius?",
                    "solution": "The formula for the area of a circle is: A = πr²"
                },
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 2,
                    "description": "Substitute the given radius into the formula",
                    "hint": "Replace r in the formula with the given radius value.",
                    "solution": "A = π(4)²\nA = π(16)\nA = 16π"
                },
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 3,
                    "description": "Calculate the final answer",
                    "hint": "Use 3.14 or 3.14159 as an approximation for π if a decimal answer is needed.",
                    "solution": "A = 16π\nA ≈ 16 × 3.14159\nA ≈ 50.27 cm²"
                }
            ],
            "related_goals": ["G9", "G10"]  # IDs from curriculum setup
        },
        {
            "id": str(uuid.uuid4()),
            "text": "Simplify the expression: 3(2x - 4) + 5x",
            "subject_area": "Algebra",
            "difficulty": 2,
            "user_id": None,
            "steps": [
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 1,
                    "description": "Apply the distributive property",
                    "hint": "Use the distributive property to multiply 3 by each term inside the parentheses.",
                    "solution": "3(2x - 4) + 5x\n= 3 × 2x - 3 × 4 + 5x\n= 6x - 12 + 5x"
                },
                {
                    "id": str(uuid.uuid4()),
                    "step_number": 2,
                    "description": "Combine like terms",
                    "hint": "Identify terms with the same variable and combine them.",
                    "solution": "6x - 12 + 5x\n= (6x + 5x) - 12\n= 11x - 12"
                }
            ],
            "related_goals": ["G7", "G8"]  # IDs from curriculum setup
        }
    ]
    
    # Add problems and solution steps to Neo4j
    for problem in sample_problems:
        # Create problem node
        neo4j_instance.run_query(
            """
            CREATE (p:Problem {
                id: $id,
                text: $text,
                subject_area: $subject_area,
                difficulty: $difficulty,
                user_id: $user_id,
                created_at: datetime()
            })
            """,
            {
                "id": problem["id"],
                "text": problem["text"],
                "subject_area": problem["subject_area"],
                "difficulty": problem["difficulty"],
                "user_id": problem["user_id"]
            }
        )
        
        # Create solution steps
        for step in problem["steps"]:
            neo4j_instance.run_query(
                """
                MATCH (p:Problem {id: $problem_id})
                CREATE (s:SolutionStep {
                    id: $id,
                    step_number: $step_number,
                    description: $description,
                    hint: $hint,
                    solution: $solution,
                    user_solved: false,
                    solved_with_hint: null
                })
                CREATE (p)-[:HAS_STEP]->(s)
                """,
                {
                    "problem_id": problem["id"],
                    "id": step["id"],
                    "step_number": step["step_number"],
                    "description": step["description"],
                    "hint": step["hint"],
                    "solution": step["solution"]
                }
            )
            
            # Link steps to curriculum goals
            for goal_id in problem["related_goals"]:
                neo4j_instance.run_query(
                    """
                    MATCH (s:SolutionStep {id: $step_id})
                    MATCH (g:Goal {id: $goal_id})
                    CREATE (s)-[:RELATED_TO_GOAL]->(g)
                    """,
                    {
                        "step_id": step["id"],
                        "goal_id": goal_id
                    }
                )
    
    logger.info(f"Created {len(sample_problems)} sample problems with solution steps")


def create_sample_problem_history(db: Session, users: List[User]) -> None:
    """Create sample problem history for testing"""
    
    # Check if problem history already exists
    existing_history = db.query(ProblemHistory).count()
    if existing_history > 0:
        logger.info(f"Found {existing_history} existing problem history entries, skipping sample creation")
        return
    
    # Get problems from Neo4j
    problems = neo4j_db.run_query("MATCH (p:Problem) RETURN p.id as id")
    if not problems:
        logger.warning("No problems found in Neo4j, cannot create sample problem history")
        return
    
    # Create sample problem history for each user
    problem_history_entries = []
    
    for user in users:
        for i, problem in enumerate(problems):
            # Create problem history with random data
            import random
            completed = random.choice([True, False])
            steps_completed = random.randint(1, 3) if completed else random.randint(0, 2)
            steps_with_hints = random.randint(0, steps_completed)
            
            problem_history_entries.append(
                ProblemHistory(
                    user_id=user.id,
                    problem_id=problem["id"],
                    attempted_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                    completed=completed,
                    time_spent_seconds=random.randint(60, 600),
                    steps_completed=steps_completed,
                    steps_with_hints=steps_with_hints
                )
            )
    
    # Add to database
    for history in problem_history_entries:
        db.add(history)
    
    db.commit()
    logger.info(f"Created {len(problem_history_entries)} sample problem history entries")


def create_all_sample_data(db: Session):
    """Create all sample data for testing"""
    logger.info("Starting sample data creation")
    
    # Create sample data in sequence
    users = create_sample_users(db)
    create_sample_goal_progress(db, users)
    create_sample_problems(neo4j_db)
    create_sample_problem_history(db, users)
    
    logger.info("Completed sample data creation")