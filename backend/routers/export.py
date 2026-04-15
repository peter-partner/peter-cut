from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from utils.file_manager import get_output_path

router = APIRouter(prefix="/api", tags=["export"])


@router.get("/export/{job_id}")
async def download_video(job_id: str):
    """Download the finished edited video for a completed job."""
    output = get_output_path(job_id)
    if not output.exists():
        raise HTTPException(
            status_code=404,
            detail="Output video not found. Make sure the job has completed successfully.",
        )
    return FileResponse(
        path=str(output),
        media_type="video/mp4",
        filename=f"autocut_{job_id}.mp4",
    )
