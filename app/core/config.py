USE_ADVANCED_SECURITY = False
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()  # Cargar las variables del archivo .env
templates = Jinja2Templates(directory="app/templates")

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
