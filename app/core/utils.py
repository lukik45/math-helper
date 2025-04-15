import os
import uuid
import json
from typing import Any, Dict, List, Optional

from loguru import logger


def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure a directory exists, create it if it doesn't"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")


def load_json_file(file_path: str, default_value: Any = None) -> Any:
    """Load data from a JSON file"""
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return default_value
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {str(e)}")
        return default_value


def save_json_file(file_path: str, data: Any) -> bool:
    """Save data to a JSON file"""
    try:
        directory = os.path.dirname(file_path)
        if directory:
            ensure_directory_exists(directory)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {str(e)}")
        return False


def parse_solution_steps(solution_text: str) -> List[Dict[str, str]]:
    """
    Parse a solution text into steps.
    
    Expected format:
    STEP 1: [Step description]
    HINT: [Hint that helps solve this step]
    SOLUTION: [Complete solution for this step]
    
    STEP 2: ...
    """
    steps = []
    current_step = {}
    step_number = 0
    
    # Split by lines and process
    lines = solution_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.upper().startswith('STEP '):
            # Save previous step if exists
            if current_step and 'description' in current_step:
                steps.append(current_step)
            
            # Start new step
            step_number += 1
            current_step = {
                'step_number': step_number,
                'description': line.split(':', 1)[1].strip() if ':' in line else '',
                'hint': '',
                'solution': ''
            }
        elif line.upper().startswith('HINT:'):
            if current_step:
                current_step['hint'] = line.split(':', 1)[1].strip() if ':' in line else ''
        elif line.upper().startswith('SOLUTION:'):
            if current_step:
                current_step['solution'] = line.split(':', 1)[1].strip() if ':' in line else ''
        else:
            # Append to the last field
            if current_step:
                if current_step['solution']:
                    current_step['solution'] += '\n' + line
                elif current_step['hint']:
                    current_step['hint'] += '\n' + line
                elif current_step['description']:
                    current_step['description'] += '\n' + line
    
    # Add the last step
    if current_step and 'description' in current_step:
        steps.append(current_step)
    
    return steps