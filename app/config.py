import os
from dotenv import dotenv_values

# Load the key from the .env file in the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
config = dotenv_values(env_path)

OPENAI_API_KEY = config.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(f"OPENAI_API_KEY not found in .env at {env_path}")
