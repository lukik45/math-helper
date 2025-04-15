from loguru import logger
import os

# Import database modules
from app.db.postgres import init_postgres_db, SessionLocal
from app.db.neo4j import init_neo4j_db


def init_db(create_sample_data=False):
    """Initialize all database connections"""
    logger.info("Initializing databases...")
    
    try:
        # Initialize PostgreSQL
        init_postgres_db()
        
        # Initialize Neo4j
        init_neo4j_db()
        
        # Create sample data if requested
        if create_sample_data:
            # Import here to avoid circular imports
            from app.db.sample_data import create_all_sample_data
            
            # Create DB session for sample data
            db = SessionLocal()
            try:
                create_all_sample_data(db)
            finally:
                db.close()
        
        logger.info("All database connections established successfully")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {str(e)}")
        raise


def should_create_sample_data():
    """Check if sample data should be created"""
    # Check environment variable
    sample_data_env = os.getenv("CREATE_SAMPLE_DATA", "false").lower()
    return sample_data_env in ("true", "1", "yes")


# Export base models and session utilities for convenience
from app.db.postgres import Base, get_db
from app.db.neo4j import neo4j_db