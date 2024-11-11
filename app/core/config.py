from pydantic_settings import BaseSettings
import os

db_url = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    DATABASE_URL: str = db_url
    testing: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
