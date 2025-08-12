from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    TOKEN: str
    REDIS: str = "redis"
    ACTORS: str = None
    DIRECTORS: str = None
    SCENARISTS: str = None
    PRODUCTION: str = None
    ADMINS: List[int]

    class Config:
        env_file = ".env"

settings = Settings()