# AI Math Tutor

An intelligent learning platform designed specifically for students struggling with mathematics. The application connects problem-solving steps with curriculum requirements from the Polish educational system, helping students identify and address knowledge gaps through personalized learning.

## Core Features

- **Step-by-step guided learning** with hints before solutions
- **Curriculum-aligned explanations** mapped to the Polish core curriculum
- **Knowledge gap identification** through interactive problem-solving
- **Personalized learning experience** that adapts to student difficulties

## Project Architecture

### Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit (for rapid MVP development)
- **Databases**:
  - Neo4j: Knowledge graph for curriculum, problems, solutions, and their relationships
  - PostgreSQL: User account management and authentication
- **AI Integration**: OpenAI API for problem-solving and curriculum matching

### System Architecture

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│               │      │               │      │               │
│   Streamlit   │<─────┤   FastAPI     │<─────┤   OpenAI API  │
│   Frontend    │      │   Backend     │      │               │
│               │      │               │      │               │
└───────┬───────┘      └───────┬───────┘      └───────────────┘
        │                      │
        │                      │
┌───────▼───────┐      ┌───────▼───────┐
│               │      │               │
│  PostgreSQL   │      │    Neo4j      │
│  User Data    │      │  Knowledge    │
│               │      │    Graph      │
└───────────────┘      └───────────────┘
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Neo4j
- OpenAI API key

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/ai-math-tutor.git
   cd ai-math-tutor
   ```

2. Set up a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create `.env` file with your environment variables
   ```
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # Security
   SECRET_KEY=your_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   
   # PostgreSQL
   POSTGRES_USER=yourusername
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=aimathtutordb
   
   # Neo4j
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=yourpassword
   
   # OpenAI
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run migrations (once database setup is implemented)
   ```
   alembic upgrade head
   ```

### Running the Application

1. Start the FastAPI backend
   ```
   cd app
   uvicorn main:app --reload
   ```

2. Start the Streamlit frontend
   ```
   cd frontend
   streamlit run 1_🏠_Home.py
   ```

### Docker Deployment

1. Build and start the containers
   ```
   docker-compose up -d
   ```

## Development

### Project Structure

- `app/`: FastAPI backend
  - `api/`: API routes
  - `core/`: Core configuration and utilities
  - `db/`: Database connections
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic schemas
  - `services/`: Business logic

- `frontend/`: Streamlit frontend
  - `pages/`: Streamlit pages
  - `components/`: Reusable UI components
  - `utils/`: Utility functions

- `tests/`: Test suite

### Running Tests

```
pytest
```

### Contributing

1. Create a feature branch
   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests
   ```
   pytest
   ```

4. Push to your branch
   ```
   git push origin feature/your-feature-name
   ```

5. Create a pull request

## License

[MIT](LICENSE)