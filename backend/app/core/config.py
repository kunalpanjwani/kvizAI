"""
Configuration settings for kvizAI Backend
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "kvizAI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./kvizai.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Accept both string and list, convert string to list
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://127.0.0.1:3000"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Split comma-separated string and strip whitespace
            origins = [origin.strip() for origin in v.split(',') if origin.strip()]
            print(f"Parsed CORS origins from string: {origins}")
            return origins
        elif isinstance(v, list):
            print(f"Using CORS origins from list: {v}")
            return v
        else:
            print(f"Unexpected CORS origins type: {type(v)}, value: {v}")
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # AI Models
    GOOGLE_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_AI_MODEL: str = "llama2"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Quiz Settings
    MAX_QUESTIONS_PER_QUIZ: int = 50
    DEFAULT_QUIZ_TIME_LIMIT: int = 30  # minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 