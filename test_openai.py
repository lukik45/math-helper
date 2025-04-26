#!/usr/bin/env python3
"""
Script to test OpenAI integration with JSON response format.
This can help diagnose issues with the OpenAI API key or connectivity.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("ERROR: OPENAI_API_KEY is not set in your environment variables or .env file.")
    print("Please set your OpenAI API key and try again.")
    sys.exit(1)

# Try to import OpenAI library
try:
    from openai import OpenAI
    print("OpenAI library successfully imported.")
except ImportError:
    print("ERROR: Failed to import OpenAI library. Make sure it's installed:")
    print("pip install --upgrade openai")
    sys.exit(1)

# Create client with API key
client = OpenAI(api_key=openai_api_key)

# Test API connection with a simple completion
test_problem = "Solve: 2x + 5 = 13"

print(f"\nTesting OpenAI API with JSON mode for a sample math problem: '{test_problem}'")
print("Generating solution...\n")

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
You are a math tutor.

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

try:
    # Using the latest OpenAI client format with JSON response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Model that supports JSON mode
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Solve this math problem step by step: {test_problem}"}
        ],
        response_format={"type": "json_object"},  # Request JSON response
        temperature=0.7,
        max_tokens=1000
    )
    
    # Get the raw JSON response
    json_response = response.choices[0].message.content
    
    # Print the raw JSON response
    print("SUCCESS! Got JSON response from OpenAI API:")
    print("-" * 80)
    print(json_response)
    print("-" * 80)
    
    # Parse and pretty print the JSON
    try:
        parsed_json = json.loads(json_response)
        print("\nParsed JSON (pretty):")
        print(json.dumps(parsed_json, indent=2))
        
        # Verify steps array exists
        if "steps" in parsed_json and isinstance(parsed_json["steps"], list):
            print(f"\nSuccessfully parsed {len(parsed_json['steps'])} solution steps!")
        else:
            print("\nWARNING: JSON doesn't contain the expected 'steps' array!")
    except json.JSONDecodeError as e:
        print(f"\nWARNING: Couldn't parse the response as JSON: {e}")
    
    print("\nYour OpenAI API integration with JSON mode is working correctly.")
    print(f"API key (first 5 chars): {openai_api_key[:5]}...")
    print(f"Using model: gpt-3.5-turbo-1106")
    
except Exception as e:
    print(f"ERROR: Failed to connect to OpenAI API: {str(e)}")
    print("\nPossible reasons for failure:")
    print("1. Your API key is invalid or expired")
    print("2. You don't have access to the gpt-3.5-turbo-1106 model (required for JSON mode)")
    print("3. Network connectivity issues")
    print("4. OpenAI service might be down")
    print("\nPlease check your API key and try again.")
    sys.exit(1)