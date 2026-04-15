# Transition Sound Effects

Place the following MP3 files in this directory:

| File | Description | Style |
|------|-------------|-------|
| `whoosh.mp3` | Classic fast camera whoosh | General transitions |
| `swoosh.mp3` | Light, subtle swoosh | Subtle transitions |
| `viral_zoom.mp3` | Deep bass punch + distortion | TikTok/viral zoom |
| `impact.mp3` | Slam / thud | Hard cuts |

## Free Sources

- [freesound.org](https://freesound.org) — search "whoosh transition"
- [zapsplat.com](https://www.zapsplat.com) — free SFX library
- [pixabay.com/sound-effects](https://pixabay.com/sound-effects/) — royalty-free

## Generate Placeholder Files (for development)

If you have Python + ffmpeg installed, run:

```bash
python generate_sounds.py
```

This creates silent placeholder MP3s so the app runs without errors during development.
