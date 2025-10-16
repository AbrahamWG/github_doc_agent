from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    gemini_api_key: str
    github_token: Optional[str] = ""  # Optional for public repos
    environment: str = "development"
    frontend_url: str = "http://localhost:5173"
    backend_port: int = 8000

    # Rate limiting
    max_requests_per_minute: int = 10

    # GitHub API
    github_api_base: str = "https://api.github.com"
    max_file_size_mb: int = 1  # Skip files larger than this

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
