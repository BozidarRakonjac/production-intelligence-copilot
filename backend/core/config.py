# Centralized configuration - all env vars in one place

import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER")
LLM_MODEL = os.getenv("LLM_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Search
VECTOR_SEARCH_TOP_K = int(os.getenv("VECTOR_SEARCH_TOP_K", "10"))
KEYWORD_SEARCH_TOP_K = int(os.getenv("KEYWORD_SEARCH_TOP_K", "10"))
FINAL_TOP_K = int(os.getenv("FINAL_TOP_K", "5"))