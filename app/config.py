import os
from dotenv import load_dotenv, find_dotenv

# Load from .env locally
load_dotenv(find_dotenv())

# Always try to get from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file.")
