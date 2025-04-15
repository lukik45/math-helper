from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
import os

from app.core.config import settings

# Make sure the database directory exists
os.makedirs(os.path.dirname(os.path.abspath("./app.db")), exist_ok=True)

# Create SQLAlchemy engine with SQLite
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False,  # Set to True for debugging SQL queries
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Dependency for FastAPI endpoints to get a database session
    Usage: `db: Session = Depends(get_db)`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_sqlite_db():
    """Initialize SQLite database with all tables"""
    try:
        # Create all tables
        # Import all models here to ensure they're registered with Base
        from app.models.users import User, GoalProgress, ProblemHistory, UserSettings
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("SQLite tables created")
        
        # Check connection
        with SessionLocal() as session:
            result = session.execute(text("SELECT 1")).fetchone()
            if not result:
                raise Exception("SQLite connection test failed")
        
        logger.info("SQLite connection verified")
        
    except Exception as e:
        logger.error(f"SQLite initialization failed: {str(e)}")
        raise