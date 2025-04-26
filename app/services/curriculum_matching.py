import re
import openai
from typing import List, Dict, Any
from neo4j import GraphDatabase

from app.core.config import settings
from app.db.neo4j import get_neo4j

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def get_all_curriculum_requirements(driver=None):
    """Get all requirements from the curriculum"""
    if driver is None:
        driver = get_neo4j()
    
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Requirement)
            RETURN r.id as id, r.description as description
        """)
        
        return [dict(record) for record in result]


def get_goals_for_requirements(requirement_ids: List[str], driver=None):
    """Get goals associated with the given requirements"""
    if driver is None:
        driver = get_neo4j()
    
    with driver.session() as session:
        result = session.run("""
            MATCH (r:Requirement)-[:HAS_GOAL]->(g:Goal)
            WHERE r.id IN $requirement_ids
            RETURN g.id as id, g.description as description, 
                   r.id as requirement_id, r.description as requirement_description
        """, requirement_ids=requirement_ids)
        
        goals = {}
        for record in result:
            goal_id = record["id"]
            
            if goal_id not in goals:
                goals[goal_id] = {
                    "id": goal_id,
                    "description": record["description"],
                    "requirements": []
                }
            
            goals[goal_id]["requirements"].append({
                "id": record["requirement_id"],
                "description": record["requirement_description"]
            })
        
        return list(goals.values())


def parse_ids_from_response(response_text: str) -> List[str]:
    """Parse IDs from the LLM response"""
    # Clean up response text
    cleaned_text = response_text.strip()
    
    # Extract IDs (assuming they're comma-separated)
    ids = re.findall(r'([A-Za-z0-9_\-.]+)', cleaned_text)
    
    # Remove duplicates and clean up
    clean_ids = []
    for id_value in ids:
        # Remove trailing commas or periods
        clean_id = id_value.rstrip(',.;')
        if clean_id and clean_id not in clean_ids:
            clean_ids.append(clean_id)
    
    return clean_ids


def match_step_to_curriculum(step_description: str, step_solution: str, driver=None) -> List[Dict[str, Any]]:
    """Match a solution step to curriculum requirements and goals using LLM"""
    if driver is None:
        driver = get_neo4j()
    
    # Get all requirements from Neo4j
    requirements = get_all_curriculum_requirements(driver)
    
    # If we have no requirements, return empty
    if not requirements:
        # For MVP, let's provide some sample goals if database is empty
        return [{
            "id": "sample_goal_1",
            "description": "Use algebraic methods to solve equations",
            "requirements": [{
                "id": "req_1",
                "description": "Solve linear equations"
            }]
        }]
    
    # Format requirements for LLM context
    requirements_text = "\n".join([f"ID: {r['id']} - {r['description']}" for r in requirements])
    
    # First matching stage: Find relevant requirements
    prompt = f"""
    You are an expert in the Polish mathematics curriculum.
    
    Below is a step in solving a math problem:
    Step Description: {step_description}
    Step Solution: {step_solution}
    
    Below are curriculum requirements from the Polish math curriculum:
    {requirements_text}
    
    Identify the curriculum requirements that are most relevant to this solution step.
    Return only the IDs of the relevant requirements, separated by commas.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an education curriculum expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse requirement IDs from response
        requirement_ids = parse_ids_from_response(response.choices[0].message.content)
        
        # Get goals associated with these requirements
        if requirement_ids:
            goals = get_goals_for_requirements(requirement_ids, driver)
            return goals
        else:
            # Fallback to sample data if no matches
            return [{
                "id": "sample_goal_1",
                "description": "Use algebraic methods to solve equations",
                "requirements": [{
                    "id": "req_1",
                    "description": "Solve linear equations"
                }]
            }]
    except Exception as e:
        print(f"Error in curriculum matching: {e}")
        # Return sample data as fallback
        return [{
            "id": "sample_goal_1",
            "description": "Use algebraic methods to solve equations",
            "requirements": [{
                "id": "req_1",
                "description": "Solve linear equations"
            }]
        }]