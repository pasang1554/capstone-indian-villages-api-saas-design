from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./villages.db"
    REDIS_URL: str = ""
    API_KEY_HEADER: str = "X-API-Key"
    RATE_LIMIT_PER_MINUTE: int = 100
    USE_REDIS: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
