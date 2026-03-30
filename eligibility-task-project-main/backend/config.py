import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://taskdb:bdksat7@taskdb:5432/taskdb")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "eligibilitytasksecret98")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DEBUG = os.getenv("DEBUG", "True") == "True"

config = Config()
