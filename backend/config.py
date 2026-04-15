from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    upload_dir: Path = Path("uploads")
    output_dir: Path = Path("outputs")
    assets_dir: Path = Path("assets")

    whisper_model: str = "base"
    whisper_language: str | None = None

    max_upload_size_mb: int = 2000
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.output_dir.mkdir(parents=True, exist_ok=True)
