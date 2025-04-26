# AI Math Tutor MVP

## Overview

AI Math Tutor is an intelligent learning platform that connects problem-solving steps with curriculum requirements, helping students identify and address knowledge gaps through personalized learning.

This repository contains the MVP (Minimum Viable Product) version of the AI Math Tutor application, consisting of a FastAPI backend and Streamlit frontend.

## Core Features

- Step-by-step guided learning with hints before solutions
- Curriculum-aligned explanations mapped to the educational curriculum
- Knowledge gap identification through interactive problem-solving
- Personalized learning experience that adapts to student difficulties

## Technical Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Databases**:
  - Neo4j: Knowledge graph for curriculum, problems, solutions, and their relationships
  - SQLite: User account management and authentication (simplified for MVP)
- **AI Integration**: OpenAI API for problem-solving and curriculum matching

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Neo4j database (local or cloud instance)
- OpenAI API key

### Environment Setup

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/ai-math-tutor.git
   cd ai-math-tutor
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your_secret_key_for_jwt
   OPENAI_API_KEY=your_openai_api_key
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   ```

### Running the Application

1. **Start the backend**:
   ```
   cd app
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend**:
   ```
   cd frontend
   streamlit run pages/1_🏠_Home.py
   ```
   The Streamlit app will be available at `http://localhost:8501`

## Database Setup

### Neo4j Setup

1. Install Neo4j desktop or use a cloud instance
2. Create a new database
3. Set password and note connection details for the `.env` file
4. (Optional) Import sample curriculum data:
   ```
   // Example Cypher query to create basic curriculum structure
   CREATE (c:Chapter {id: "ch_1", name: "Algebra", grade_level: 7})
   CREATE (r:Requirement {id: "req_1", description: "Solve linear equations"})
   CREATE (g:Goal {id: "goal_1", description: "Use algebraic methods to solve linear equations"})
   CREATE (c)-[:HAS_REQUIREMENT]->(r)
   CREATE (r)-[:HAS_GOAL]->(g)
   ```

## Usage Guide

1. **Register/Login**: Create an account or log in to access the application
2. **Solve a Problem**: Enter a math problem to get a step-by-step solution
3. **Learn with Hints**: Try to solve each step with hints before viewing the solution
4. **Track Progress**: View your mastery levels and struggling areas
5. **Practice with Recommendations**: Solve recommended problems to improve in weak areas

## Project Structure

```
ai-math-tutor/
├── app/                 # Backend code
│   ├── api/             # API endpoints
│   ├── core/            # Core configuration
│   ├── db/              # Database connections
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── frontend/            # Streamlit frontend
│   ├── pages/           # Application pages
│   ├── components/      # Reusable UI components
│   └── utils/           # Utility functions
└── requirements.txt     # Project dependencies
```

## Future Enhancements

1. Enhanced curriculum matching using embeddings
2. Improved visualization for learning progress
3. Custom problem generator targeting weak areas
4. Mobile-friendly interface
5. Teacher dashboard for educators