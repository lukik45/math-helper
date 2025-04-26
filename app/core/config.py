import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Math Tutor"
    PROJECT_VERSION: str = "0.1.0"
    
    # API Settings
    API_V1_STR: str = "/api"
    
    # Secret Key for JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database Settings
    SQLITE_DATABASE_URL: str = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./mathtutor.db")
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()

# Check critical settings
if not settings.OPENAI_API_KEY:
    logger.warning("========== WARNING ==========")
    logger.warning("OPENAI_API_KEY is not set! The solution generation will not work.")
    logger.warning("Please set the OPENAI_API_KEY environment variable or add it to your .env file.")
    logger.warning("============================")

if settings.SECRET_KEY == "supersecretkey":
    logger.warning("You are using the default SECRET_KEY. This is not secure for production.")

# Log other important settings
logger.info(f"Database URL: {settings.SQLITE_DATABASE_URL}")
logger.info(f"Neo4j URI: {settings.NEO4J_URI}")
logger.info(f"API prefix: {settings.API_V1_STR}")
logger.info(f"OpenAI API key set: {bool(settings.OPENAI_API_KEY)}")  # Don't log the actual key
