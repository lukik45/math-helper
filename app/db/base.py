from loguru import logger

# Import database modules
from app.db.postgres import init_db as init_postgres
from app.db.neo4j import neo4j_db


def init_db():
    """Initialize all database connections"""
    logger.info("Initializing databases...")
    
    # Initialize PostgreSQL
    init_postgres()
    
    # Test Neo4j connection
    try:
        neo4j_db.get_driver()
        logger.info("All database connections established successfully")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {str(e)}")
        raise