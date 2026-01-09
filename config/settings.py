"""
Configuration settings for MCD 311 Sovereign Voice AI
Manages Redis, LLM, and logging configurations.
"""

import os
import logging
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global settings for the Sovereign Voice AI system.
    Loads from environment variables or .env file.
    """

    # === REDIS CONFIGURATION ===
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DECODE_RESPONSES: bool = True

    # === LANGGRAPH CONFIGURATION ===
    LANGGRAPH_CHECKPOINT_NS: str = "mcd_311_sessions"

    # === OLLAMA LLM CONFIGURATION ===
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_FAST: str = "mistral"  # Fast path model for quick responses
    OLLAMA_MODEL_DEEP: str = "neural-chat"  # Deep reasoning model
    OLLAMA_TIMEOUT: int = 30

    # === SESSION MANAGEMENT ===
    SESSION_TIMEOUT_SECONDS: int = 3600  # 1 hour session timeout
    SESSION_DATA_RETENTION_SECONDS: int = 10  # Auto-wipe after call ends

    # === LOGGING ===
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/sovereign_voice_ai.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # === SYSTEM BEHAVIOR ===
    ENABLE_MEMORY_AUDIT: bool = True
    ENABLE_DATA_SHREDDING: bool = True
    MAX_CALL_DURATION_SECONDS: int = 600  # 10 minute max call

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Initialize global settings
settings = Settings()


def setup_logging():
    """
    Setup logging configuration for the application.
    Creates logs directory if it doesn't exist.
    """
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger(__name__)


# Initialize logger
logger = setup_logging()

if __name__ == "__main__":
    logger.info("Settings initialized successfully")
    logger.info(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info(f"Ollama URL: {settings.OLLAMA_BASE_URL}")
    logger.info(f"Fast Model: {settings.OLLAMA_MODEL_FAST}")
    logger.info(f"Deep Model: {settings.OLLAMA_MODEL_DEEP}")
