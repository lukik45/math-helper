from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from loguru import logger

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    # Add common columns here as needed

Base = declarative_base(cls=Base)

def get_db():
    """
    Dependency for FastAPI endpoints to get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database with all tables
    """
    try:
        # Import all models here to ensure they're registered with Base
        # This is typically imported in the calling module
        # from app.models import users, progress
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise