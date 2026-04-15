"""Minimal API smoke tests."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
from io import BytesIO


def _client():
    from main import app
    return TestClient(app)


def test_root():
    assert _client().get("/").status_code == 200


def test_health():
    assert _client().get("/health").json()["status"] == "ok"


def test_upload_requires_file():
    assert _client().post("/api/upload").status_code == 422


def test_upload_rejects_text():
    r = _client().post("/api/upload", files={"video": ("t.txt", BytesIO(b"hi"), "text/plain")})
    assert r.status_code == 415


def test_upload_accepts_video():
    r = _client().post("/api/upload", files={"video": ("v.mp4", BytesIO(b"\x00" * 512), "video/mp4")})
    assert r.status_code == 200
    assert "job_id" in r.json()
