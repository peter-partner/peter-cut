"""
File I/O helpers for managing uploaded and processed video files.
"""

import uuid
import shutil
from pathlib import Path

from config import settings


def save_upload(file_data: bytes, original_filename: str) -> tuple[str, Path]:
    """
    Save uploaded file bytes to the upload directory with a unique job ID.
    Returns (job_id, file_path).
    """
    job_id = str(uuid.uuid4())
    ext = Path(original_filename).suffix or ".mp4"
    dest = settings.upload_dir / f"{job_id}{ext}"
    dest.write_bytes(file_data)
    return job_id, dest


def get_upload_path(job_id: str) -> Path | None:
    """Find the uploaded file for a job_id (handles any extension)."""
    matches = list(settings.upload_dir.glob(f"{job_id}.*"))
    return matches[0] if matches else None


def get_output_path(job_id: str) -> Path:
    """Return the output path for a processed video."""
    return settings.output_dir / f"{job_id}_output.mp4"


def cleanup_job(job_id: str):
    """Remove upload and output files for a job."""
    upload = get_upload_path(job_id)
    if upload and upload.exists():
        upload.unlink()
    output = get_output_path(job_id)
    if output.exists():
        output.unlink()
