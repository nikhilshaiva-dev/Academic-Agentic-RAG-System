import os
from dotenv import load_dotenv

# Base directory of the Agentic rag project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables safely from project root
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Reliable absolute paths to avoid working-directory issues
DATA_DIR = os.path.join(BASE_DIR, "data")
POLICY_DIR = os.path.join(BASE_DIR, "policies")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vectorstore")
DATABASE_PATH = os.path.join(BASE_DIR, "chat_app.db")

REFERENCE_DATE = "2025-01-15"
