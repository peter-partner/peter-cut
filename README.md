# AutoCut — Intelligent Video Editing Platform

> **ตัดต่อวิดีโออัตโนมัติด้วย AI** | Auto-edit your raw footage instantly by voice cues.

---

## Vision

AutoCut is a platform that transforms long raw video recordings into polished, ready-to-use edits — automatically. Directors, content creators, and filmmakers simply say **"Scene 1 Take 1"**, **"Scene 1 Take 2"**, and AutoCut handles the rest: it finds the best take for each scene, cuts everything else, and stitches the final video together with cinematic transitions and sound effects.

No timeline dragging. No manual cuts. Just upload and export.

---

## How It Works

1. **Record normally** — Say your scene/take cues out loud before each shot (in English or Thai)
2. **Upload** — Drop your raw footage into AutoCut
3. **Process** — AutoCut transcribes your voice cues using AI speech recognition
4. **Auto-edit** — The latest take of each scene is selected; all earlier takes are discarded
5. **Transitions** — Cinematic transitions (zoom in/out, viral distortion) are applied between scenes
6. **Export** — Download your finished video

---

## Voice Cue Format

AutoCut listens for these patterns (English and Thai):

| English | Thai |
|---------|------|
| "Scene 1 Take 1" | "ฉาก 1 เทค 1" |
| "Scene 2 Take 3" | "ฉาก 2 เทค 3" |
| "Scene one take two" | "ฉากหนึ่ง เทคสอง" |

**Logic:** For each scene, only the **last take recorded** is used in the final edit. All previous takes of that scene are automatically discarded.

---

## Features

- **AI Speech Recognition** — Powered by OpenAI Whisper (supports Thai + English)
- **Smart Take Selection** — Automatically keeps only the final take per scene
- **Cinematic Transitions**
  - Zoom In / Zoom Out
  - Distorted Viral Zoom (popular social media style)
  - Cut (instant)
  - Fade
- **Transition Sound Effects** — Whoosh, swoosh, and impact sounds
- **Thai Language UI** — Full Thai interface
- **Web-based** — No software installation required
- **REST API** — Integrate AutoCut into your own workflow

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11 + FastAPI |
| Video Processing | MoviePy + FFmpeg |
| Speech Recognition | OpenAI Whisper (large-v3) |
| Frontend | React 18 + TypeScript + Vite |
| Styling | Tailwind CSS |
| Job Queue | Celery + Redis |
| Storage | Local filesystem (S3-compatible in production) |

---

## Project Structure

```
peter-cut/
├── README.md                    # This file
├── VISION.md                    # Product vision and roadmap
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt         # Python dependencies
│   ├── config.py                # App configuration
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── speech_detector.py   # Detect scene/take cues via Whisper
│   │   ├── scene_parser.py      # Parse cues into scene/take structure
│   │   ├── video_editor.py      # Cut, trim, and merge clips
│   │   ├── transitions.py       # Zoom, distort, fade transitions
│   │   └── audio_effects.py     # Transition sound effects
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── upload.py            # Video upload endpoint
│   │   ├── process.py           # Processing job endpoint
│   │   └── export.py            # Export/download endpoint
│   └── utils/
│       ├── __init__.py
│       └── file_manager.py      # File I/O helpers
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── i18n/
│       │   ├── th.ts            # Thai translations
│       │   └── en.ts            # English translations
│       ├── components/
│       │   ├── VideoUpload.tsx
│       │   ├── ProcessingStatus.tsx
│       │   ├── ScenePreview.tsx
│       │   ├── TransitionPicker.tsx
│       │   └── VideoPlayer.tsx
│       ├── hooks/
│       │   ├── useUpload.ts
│       │   └── useProcessing.ts
│       └── api/
│           └── client.ts
├── assets/
│   └── sounds/                  # Transition sound effects (MP3)
│       ├── whoosh.mp3
│       ├── swoosh.mp3
│       ├── viral_zoom.mp3
│       └── impact.mp3
├── docker-compose.yml
├── Dockerfile.backend
└── Dockerfile.frontend
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- FFmpeg (`sudo apt install ffmpeg` / `brew install ffmpeg`)
- Redis (for job queue)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Docker (Recommended)

```bash
docker-compose up --build
```

Open [http://localhost:3000](http://localhost:3000)

---

## API Reference

### `POST /api/upload`
Upload a raw video file.

**Request:** `multipart/form-data` with field `video`

**Response:**
```json
{
  "job_id": "abc123",
  "filename": "raw_footage.mp4",
  "duration": 1234.5
}
```

---

### `POST /api/process/{job_id}`
Start processing a uploaded video.

**Body:**
```json
{
  "transition_style": "viral_zoom",
  "transition_sound": "whoosh",
  "language": "th"
}
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "processing",
  "scenes_detected": 5
}
```

---

### `GET /api/status/{job_id}`
Poll for job status.

**Response:**
```json
{
  "job_id": "abc123",
  "status": "done",
  "progress": 100,
  "scenes": [
    { "scene": 1, "best_take": 2, "total_takes": 2, "duration": 45.2 },
    { "scene": 2, "best_take": 1, "total_takes": 1, "duration": 30.1 }
  ]
}
```

---

### `GET /api/export/{job_id}`
Download the finished video.

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss what you'd like to change.

---

## License

MIT

---

*Built with love for creators in Thailand and worldwide.*
