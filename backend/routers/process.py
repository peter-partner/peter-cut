"""
Processing endpoints — start and poll video editing jobs.

Jobs run in a background thread (simple for MVP; swap for Celery in production).
"""

import threading
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

from utils.file_manager import get_upload_path, get_output_path
from processors.speech_detector import SpeechDetector
from processors.scene_parser import build_scene_plan
from processors.video_editor import edit_video, probe_duration
from config import settings

router = APIRouter(prefix="/api", tags=["process"])

# In-memory job store (replace with Redis/DB in production)
_jobs: dict[str, dict] = {}
_detector: SpeechDetector | None = None


def _get_detector() -> SpeechDetector:
    global _detector
    if _detector is None:
        _detector = SpeechDetector(model_name=settings.whisper_model)
    return _detector


class ProcessRequest(BaseModel):
    transition_style: Literal["cut", "fade", "zoom_in", "zoom_out", "viral_zoom"] = "viral_zoom"
    transition_sound: Literal["whoosh", "swoosh", "viral_zoom", "impact", "none"] = "whoosh"
    language: Literal["th", "en"] | None = None  # None = auto-detect


class ProcessResponse(BaseModel):
    job_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "done", "error"]
    progress: int
    message: str
    scenes: list[dict] | None = None
    error: str | None = None


def _run_job(job_id: str, req: ProcessRequest):
    """Background thread: run the full pipeline for a job."""
    job = _jobs[job_id]

    def progress(pct: int, msg: str):
        job["progress"] = pct
        job["message"] = msg

    try:
        job["status"] = "processing"
        progress(5, "กำลังเริ่มต้น... / Starting...")

        upload_path = get_upload_path(job_id)
        if not upload_path:
            raise FileNotFoundError(f"Upload not found for job {job_id}")

        # Step 1: Detect video duration
        duration = probe_duration(upload_path)
        progress(10, "วิเคราะห์เสียง... / Analysing audio...")

        # Step 2: Detect scene/take cues
        detector = _get_detector()
        cues = detector.detect_cues(str(upload_path), language=req.language)
        progress(50, f"พบสัญญาณ {len(cues)} จุด / Found {len(cues)} cue(s)")

        if not cues:
            raise ValueError(
                "ไม่พบสัญญาณ scene/take ในวิดีโอ / No scene/take cues detected. "
                "Make sure you say 'Scene X Take Y' before each shot."
            )

        # Step 3: Build scene plan
        plan = build_scene_plan(cues, duration)
        job["scenes"] = [
            {
                "scene": c.scene,
                "best_take": c.take,
                "start": round(c.start, 2),
                "end": round(c.end, 2),
                "duration": round(c.duration, 2),
            }
            for c in plan.selected_clips
        ]
        progress(55, f"แผนการตัดต่อ: {len(plan.selected_clips)} ฉาก / Edit plan: {len(plan.selected_clips)} scene(s)")

        # Step 4: Edit video
        output_path = get_output_path(job_id)
        edit_video(
            source_path=upload_path,
            scene_plan=plan,
            output_path=output_path,
            transition_style=req.transition_style,
            transition_sound=req.transition_sound,
            assets_dir=str(settings.assets_dir / "sounds"),
            progress_callback=lambda pct, msg: progress(55 + int(pct * 0.45), msg),
        )

        job["status"] = "done"
        job["progress"] = 100
        job["message"] = "เสร็จสิ้น! / Done! Your video is ready."

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        job["message"] = f"เกิดข้อผิดพลาด: {e}"
        print(f"[process] Job {job_id} failed: {e}")


@router.post("/process/{job_id}", response_model=ProcessResponse)
async def start_processing(job_id: str, req: ProcessRequest = ProcessRequest()):
    """Start processing a previously uploaded video."""
    if not get_upload_path(job_id):
        raise HTTPException(status_code=404, detail="Job not found. Please upload a video first.")

    if job_id in _jobs and _jobs[job_id]["status"] in ("processing", "done"):
        raise HTTPException(status_code=409, detail="Job already running or completed.")

    _jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "รอดำเนินการ... / Queued...",
        "scenes": None,
        "error": None,
    }

    thread = threading.Thread(target=_run_job, args=(job_id, req), daemon=True)
    thread.start()

    return ProcessResponse(
        job_id=job_id,
        status="queued",
        message="เริ่มประมวลผล / Processing started",
    )


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """Poll the status of a processing job."""
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found.")

    job = _jobs[job_id]
    return StatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job.get("progress", 0),
        message=job.get("message", ""),
        scenes=job.get("scenes"),
        error=job.get("error"),
    )
