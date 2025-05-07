import os
import streamlit as st
from dotenv import dotenv_values

# Load .env for local dev
env_path = os.path.join(os.path.dirname(__file__), '.env')
env_config = dotenv_values(env_path)

# Streamlit secrets (Cloud deployment)
secret_key = None
try:
    secret_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass

# Fall back to .env if not using secrets
OPENAI_API_KEY = secret_key or env_config.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in Streamlit secrets or .env file.")
