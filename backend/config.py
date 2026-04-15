from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Paths
    upload_dir: Path = Path("uploads")
    output_dir: Path = Path("outputs")
    assets_dir: Path = Path("../assets")

    # Whisper
    whisper_model: str = "base"  # Options: tiny, base, small, medium, large-v3
    whisper_language: str | None = None  # None = auto-detect

    # Redis / Celery
    redis_url: str = "redis://localhost:6379/0"

    # API
    max_upload_size_mb: int = 2000  # 2 GB
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()

# Ensure directories exist
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.output_dir.mkdir(parents=True, exist_ok=True)
