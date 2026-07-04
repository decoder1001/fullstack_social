from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://ross:Badonkadonk56@localhost:5432/socialdb"
    PROJECT_NAME: str = "Fullstack_Social"

class Config:
    env_file = ".env"
    extra = "ignore"

settings = Settings()
