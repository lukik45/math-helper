import json
import logging
from typing import List, Dict, Any
from openai import OpenAI

from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client with the API key from settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_solution(problem_text: str, grade_level: int = None) -> List[Dict[str, str]]:
    """Generate a step-by-step solution for a math problem using the latest OpenAI API with JSON response"""
    logger.info(f"Generating solution for problem: {problem_text}")
    
    if not settings.OPENAI_API_KEY:
        logger.error("OpenAI API key is not set! Check your environment variables.")
        return []
    
    grade_context = f"for grade {grade_level}" if grade_level else ""
    
    # Define the JSON response format we want
    json_format = """
    {
        "steps": [
            {
                "step_number": 1,
                "description": "Description of what this step does",
                "hint": "A hint that helps without giving away the full solution",
                "solution": "The complete solution for this step"
            },
            {
                "step_number": 2,
                "description": "...",
                "hint": "...",
                "solution": "..."
            }
        ]
    }
    """
    
    system_message = f"""
    You are a math tutor specializing in the Polish curriculum.
    
    You will receive a math problem to solve. Provide a step-by-step solution
    in the JSON format shown below. Make sure your JSON is valid and follows this
    exact structure:
    
    {json_format}
    
    Break down the solution into clear, logical steps. Each step should have:
    1. A description of what this step accomplishes
    2. A hint that guides the student without giving away the full solution
    3. The complete solution for the step
    
    Your response must be valid JSON only, with no additional text before or after.
    """
    
    prompt = f"Solve this Polish math problem step by step {grade_context}: {problem_text}"
    
    try:
        logger.info("Calling OpenAI API with JSON response format...")
        
        # Using the latest OpenAI client format with response_format=json_object
        response = client.chat.completions.create(
            model="o3-mini",  # This model supports JSON mode
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},  # Request JSON response
            max_completion_tokens=5000
        )
        
        logger.info("OpenAI API response received successfully")
        
        # Get the solution JSON from the response
        solution_json_text = response.choices[0].message.content
        
        logger.info(f"JSON response received, parsing...")
        
        try:
            # Parse the JSON response
            solution_data = json.loads(solution_json_text)
            
            # Extract the steps array
            if "steps" in solution_data and isinstance(solution_data["steps"], list):
                steps = solution_data["steps"]
                logger.info(f"Successfully parsed {len(steps)} solution steps from JSON")
                return steps
            else:
                logger.error("JSON response did not contain the expected 'steps' array")
                # Fall back to a single step with the raw content
                return [{
                    "step_number": 1,
                    "description": "Solution",
                    "hint": "Review the solution carefully",
                    "solution": solution_json_text
                }]
                
        except json.JSONDecodeError as json_err:
            logger.error(f"Failed to parse JSON response: {json_err}")
            logger.error(f"Raw response: {solution_json_text}")
            # Return a single step with the raw text as fallback
            return [{
                "step_number": 1,
                "description": "Complete solution",
                "hint": "Try to solve the problem step by step",
                "solution": solution_json_text
            }]
            
    except Exception as e:
        logger.error(f"Error generating solution: {str(e)}")
        # Log the full exception details
        import traceback
        logger.error(traceback.format_exc())
        return []