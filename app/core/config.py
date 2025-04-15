import os
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    PROJECT_NAME: str = "AI Math Tutor"
    
    # CORS Settings - default to allowing local development URLs
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:8501", "http://localhost:8000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                # Handle JSON-formatted string: '["http://localhost", "https://localhost"]'
                import json
                return json.loads(v)
            else:
                # Handle comma-separated string: "http://localhost,https://localhost"
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        # Default to allowing localhost if value is invalid
        return ["http://localhost:8501", "http://localhost:8000"]

    # Security
    SECRET_KEY: str = "your_secret_key_change_this_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    # Using SQLite instead of PostgreSQL
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"
    

    # Neo4j - Explicitly use localhost and default Neo4j credentials
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    # OpenAI
    OPENAI_API_KEY: str = "your_openai_api_key_here"


# Create settings instance
settings = Settings()