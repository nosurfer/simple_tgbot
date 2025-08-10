from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    TOKEN: str
    ADMINS: List[int]

    class Config:
        env_file = ".env"

settings = Settings()