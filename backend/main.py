"""
AutoCut — Intelligent Video Editing Platform
FastAPI backend entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import upload, process, export

app = FastAPI(
    title="AutoCut API",
    description="ระบบตัดต่อวิดีโออัตโนมัติ / Automatic video editing platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(process.router)
app.include_router(export.router)


@app.get("/")
async def root():
    return {
        "service": "AutoCut API",
        "version": "0.1.0",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
