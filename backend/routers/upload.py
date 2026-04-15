from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path

from utils.file_manager import save_upload
from config import settings

router = APIRouter(prefix="/api", tags=["upload"])


class UploadResponse(BaseModel):
    job_id: str
    filename: str
    size_mb: float
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_video(video: UploadFile = File(...)):
    """
    Upload a raw video file for processing.

    Returns a job_id to use in subsequent /process and /status calls.
    """
    allowed_types = {
        "video/mp4", "video/quicktime", "video/x-msvideo",
        "video/x-matroska", "video/webm", "video/mpeg",
    }

    if video.content_type and video.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {video.content_type}. Upload a video file.",
        )

    data = await video.read()
    size_mb = len(data) / (1024 * 1024)

    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {size_mb:.1f} MB. Max: {settings.max_upload_size_mb} MB.",
        )

    job_id, file_path = save_upload(data, video.filename or "upload.mp4")

    return UploadResponse(
        job_id=job_id,
        filename=video.filename or "upload.mp4",
        size_mb=round(size_mb, 2),
        message="อัปโหลดสำเร็จ / Upload successful",
    )
