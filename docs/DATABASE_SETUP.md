# Database Setup Guide

This guide explains how to set up and configure the databases for the AI Math Tutor application.

## Database Architecture

The application uses two databases:

1. **PostgreSQL**: For user account management and progress tracking
   - Stores user information, authentication data, and learning progress
   - Handles relational data like user-goal relationships

2. **Neo4j**: For curriculum knowledge graph and problem-solving data
   - Stores the curriculum structure (chapters, requirements, goals)
   - Manages problems, solution steps, and their relationships to curriculum goals
   - Enables semantic matching of problem steps to educational goals

## Setting Up PostgreSQL

### Local Development

1. Install PostgreSQL:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS with Homebrew
   brew install postgresql
   
   # Windows
   # Download the installer from https://www.postgresql.org/download/windows/
   ```

2. Create a database:
   ```bash
   sudo -u postgres psql
   
   # In the PostgreSQL prompt
   CREATE DATABASE aimathtutordb;
   CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE aimathtutordb TO your_username;
   \q
   ```

3. Update your `.env` file with the database credentials:
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=aimathtutordb
   ```

### Using Docker

If you're using Docker, the database will be automatically set up with the credentials specified in your `.env` file when you run:

```bash
docker-compose up -d postgres
```

## Setting Up Neo4j

### Local Development

1. Install Neo4j:
   ```bash
   # Download from https://neo4j.com/download/
   # Follow the installation instructions for your operating system
   ```

2. Configure Neo4j:
   - Set a password for the default user (`neo4j`)
   - Make sure the Bolt connector is enabled on port 7687

3. Update your `.env` file:
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   ```

### Using Docker

With Docker, Neo4j will be set up automatically:

```bash
docker-compose up -d neo4j
```

Access the Neo4j browser at http://localhost:7474 with the credentials from your `.env` file.

## Curriculum Structure

The application needs a curriculum structure in Neo4j. You can test and create the structure using:

```bash
python scripts/test_db_connection.py
```

If the structure doesn't exist, you'll be prompted to create a sample structure.

## Sample Data

To load sample data for testing and development:

1. Set the environment variable in your `.env` file:
   ```
   CREATE_SAMPLE_DATA=true
   ```

2. Start the application, which will create:
   - Sample users
   - Curriculum structure
   - Example math problems with solutions
   - Goal progress records

## Database Schema

### PostgreSQL Tables

- **users**: User authentication and profile information
- **goal_progress**: Tracks user mastery levels for curriculum goals
- **problem_history**: Records of user interactions with problems
- **user_settings**: User preferences and settings

### Neo4j Nodes and Relationships

Nodes:
- **Chapter**: Chapters in the Polish math curriculum
- **Requirement**: Specific requirements from the curriculum
- **Goal**: Educational goals associated with requirements
- **Problem**: Mathematical problems
- **SolutionStep**: Individual steps in problem solutions

Relationships:
- `(:Chapter)-[:HAS_REQUIREMENT]->(:Requirement)`: Links chapters to requirements
- `(:Requirement)-[:HAS_GOAL]->(:Goal)`: Links requirements to educational goals
- `(:Problem)-[:HAS_STEP]->(:SolutionStep)`: Connects problems to their solution steps
- `(:SolutionStep)-[:RELATED_TO_GOAL]->(:Goal)`: Links solution steps to curriculum goals

## Troubleshooting

### PostgreSQL Connection Issues

1. Check if PostgreSQL is running:
   ```bash
   sudo systemctl status postgresql
   # or on macOS
   brew services list
   ```

2. Verify your credentials:
   ```bash
   psql -U your_username -h localhost -d aimathtutordb
   ```

3. Check PostgreSQL logs:
   ```bash
   sudo tail -f /var/log/postgresql/postgresql-*.log
   ```

### Neo4j Connection Issues

1. Verify Neo4j is running:
   ```bash
   neo4j status
   # or in Docker
   docker ps | grep neo4j
   ```

2. Check if you can access the Neo4j browser at http://localhost:7474

3. Try connecting with the Neo4j CLI:
   ```bash
   cypher-shell -u neo4j -p your_password
   ```

4. Look at Neo4j logs:
   ```bash
   tail -f <neo4j-home>/logs/neo4j.log
   # or in Docker
   docker logs neo4j
   ```