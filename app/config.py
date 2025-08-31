from pydantic_settings import BaseSettings # - para cargar variables de entorno en una clase tipada
from pathlib import Path # - para manejar rutas y ubicar el archivo .env

class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_URL: str
    DB_NAME: str
    COLLECTION_NAME: str
    OPEN_ROUTER: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"

settings = Settings()   