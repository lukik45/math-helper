#!/usr/bin/env python3
"""
Script to set up project directory structure and initialize files
"""

import os
import sys
from pathlib import Path

# Define the directory structure
directories = [
    'app',
    'app/api',
    'app/core',
    'app/db',
    'app/models',
    'app/schemas',
    'app/services',
    'frontend',
    'frontend/pages',
    'frontend/components',
    'frontend/utils',
    'scripts',
]

def setup_project_structure():
    """Create necessary directories and __init__.py files"""
    print("Setting up project directory structure...")
    
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    
    # Create directories and __init__.py files
    for directory in directories:
        dir_path = project_root / directory
        
        # Create directory if it doesn't exist
        dir_path.mkdir(exist_ok=True, parents=True)
        print(f"Directory created (if it didn't exist): {directory}")
        
        # Create __init__.py in Python directories
        if directory.startswith('app'):
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                with open(init_file, 'w') as f:
                    f.write('# Initialize module\n')
                print(f"Created: {directory}/__init__.py")
    
    print("Project structure setup complete.")

if __name__ == "__main__":
    setup_project_structure()