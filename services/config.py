"""
Configuration module for Azure services and OpenAI settings.
Loads environment variables from .env file.
"""
import os
from services.logger_config import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()  # Loads values from .env into environment variables

logger.info("Loading environment variables...")

# Azure Document Intelligence credentials
DOCUMENT_ENDPOINT = os.getenv("DOCUMENT_ENDPOINT")
DOCUMENT_KEY = os.getenv("DOCUMENT_KEY")

# Azure OpenAI credentials
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0

logger.info("Environment variables loaded successfully")
