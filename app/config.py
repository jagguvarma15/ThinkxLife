import os
from dotenv import load_dotenv

# Load .env for local dev (safe to call even on Render)
load_dotenv()

# Try to get from environment variable (Render) or fallback to .env (local)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment or .env file.")
