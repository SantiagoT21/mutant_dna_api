from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    testing: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
