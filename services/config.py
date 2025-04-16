import os
from dotenv import load_dotenv

load_dotenv()  # Loads values from .env into environment variables

DOCUMENT_ENDPOINT = os.getenv("DOCUMENT_ENDPOINT")
DOCUMENT_KEY = os.getenv("DOCUMENT_KEY")

OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
