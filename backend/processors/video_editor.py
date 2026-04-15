"""
Core video editing engine — pure FFmpeg, no MoviePy.

Pipeline:
  1. Extract selected clips from source (stream-copy — instant, no re-encode)
  2. Build FFmpeg filter_complex for transitions between clips
  3. Mix transition sound effects
  4. Single-pass export to output MP4
"""

import json
import subprocess
import tempfile
from pathlib import Path

from .scene_parser import ScenePlan

TRANSITION_DURATION = {
    "cut": 0.0,
    "fade": 0.5,
    "zoom_in": 0.4,
    "zoom_out": 0.4,
    "viral_zoom": 0.25,
}

SOUND_MAP = {
    "whoosh": "whoosh.mp3",
    "swoosh": "swoosh.mp3",
    "viral_zoom": "viral_zoom.mp3",
    "impact": "impact.mp3",
    "none": None,
}


def probe_duration(path: str | Path) -> float:
    """Get video duration in seconds via ffprobe."""
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(r.stdout)["format"]["duration"])


def _extract_clip(source: Path, start: float, end: float, out: Path):
    """Extract a clip with stream-copy (fast, no re-encode)."""
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(start), "-to", str(end),
        "-i", str(source), "-c", "copy", "-avoid_negative_ts", "make_zero",
        str(out),
    ], capture_output=True, check=True)


def edit_video(
    source_path: str | Path,
    scene_plan: ScenePlan,
    output_path: str | Path,
    transition_style: str = "viral_zoom",
    transition_sound: str = "whoosh",
    assets_dir: str | Path = "../assets/sounds",
    progress_callback=None,
) -> Path:
    source_path = Path(source_path)
    output_path = Path(output_path)
    selected = scene_plan.selected_clips

    if not selected:
        raise ValueError("No scenes in plan.")

    def progress(pct: int, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    trans_dur = TRANSITION_DURATION.get(transition_style, 0.0)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Step 1: Extract each selected take as a separate file (stream-copy = fast)
        clip_paths: list[Path] = []
        for i, take in enumerate(selected):
            clip_path = tmpdir / f"clip_{i:03d}.mp4"
            _extract_clip(source_path, take.start, take.end, clip_path)
            clip_paths.append(clip_path)
            progress(int(30 * (i + 1) / len(selected)), f"Cut scene {take.scene}")

        # Step 2: Build FFmpeg command with filter_complex for transitions
        if len(clip_paths) == 1 or transition_style == "cut" or trans_dur == 0:
            # Simple concat — no transitions needed
            _concat_clips(clip_paths, output_path, tmpdir)
            progress(80, "Concatenated")
        else:
            _concat_with_transitions(
                clip_paths, output_path, transition_style, trans_dur,
            )
            progress(80, "Transitions applied")

        # Step 3: Mix transition sound effects
        sound_file_name = SOUND_MAP.get(transition_sound)
        if sound_file_name and len(selected) > 1:
            sound_path = Path(assets_dir) / sound_file_name
            if sound_path.exists():
                _mix_sounds(output_path, sound_path, selected, trans_dur, tmpdir)
                progress(95, "Sound effects mixed")

    progress(100, "Done")
    return output_path


def _concat_clips(clip_paths: list[Path], output: Path, tmpdir: Path):
    """Concatenate clips via concat demuxer (no re-encode when formats match)."""
    list_file = tmpdir / "concat.txt"
    list_file.write_text(
        "\n".join(f"file '{p}'" for p in clip_paths)
    )
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-c", "copy", str(output),
    ], capture_output=True, check=True)


def _concat_with_transitions(
    clip_paths: list[Path],
    output: Path,
    style: str,
    dur: float,
):
    """
    Use FFmpeg xfade filter for transitions between clips.
    Supports: fade, zoom-in (wipeleft), zoom-out (wiperight), viral_zoom (zoomin).
    """
    # Map our style names to FFmpeg xfade transition names
    xfade_map = {
        "fade": "fade",
        "zoom_in": "smoothup",
        "zoom_out": "smoothdown",
        "viral_zoom": "zoomin",
    }
    xfade_name = xfade_map.get(style, "fade")

    n = len(clip_paths)
    inputs = []
    for p in clip_paths:
        inputs += ["-i", str(p)]

    filter_parts = []
    audio_parts = []
    durations = [probe_duration(p) for p in clip_paths]

    # Track the running output duration to compute xfade offsets.
    # After each xfade the output duration = previous_output_dur + next_clip_dur - transition_dur
    prev_v = "[0:v]"
    prev_a = "[0:a]"
    output_dur = durations[0]

    for i in range(1, n):
        offset = output_dur - dur  # xfade starts `dur` seconds before the current output ends

        out_v = f"[v{i}]" if i < n - 1 else "[vout]"
        out_a = f"[a{i}]" if i < n - 1 else "[aout]"

        filter_parts.append(
            f"{prev_v}[{i}:v]xfade=transition={xfade_name}:duration={dur}:offset={offset:.4f}{out_v}"
        )
        audio_parts.append(
            f"{prev_a}[{i}:a]acrossfade=d={dur}{out_a}"
        )
        prev_v = out_v
        prev_a = out_a
        output_dur = offset + dur + (durations[i] - dur)  # = offset + durations[i]

    filter_str = ";".join(filter_parts + audio_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(output),
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def _mix_sounds(
    video_path: Path,
    sound_path: Path,
    selected_clips,
    trans_dur: float,
    tmpdir: Path,
):
    """Mix transition sound effects at each scene boundary."""
    # Calculate timestamps where transitions happen in the output video
    timestamps: list[float] = []
    cumulative = 0.0
    for i, clip in enumerate(selected_clips):
        if i > 0:
            timestamps.append(cumulative)
        cumulative += clip.duration
        if i > 0:
            cumulative -= trans_dur  # transitions overlap

    if not timestamps:
        return

    tmp_out = tmpdir / "with_sfx.mp4"

    # Build amerge filter: delay each sound to its timestamp and mix all together
    inputs = ["-i", str(video_path)]
    for _ in timestamps:
        inputs += ["-i", str(sound_path)]

    filter_parts = []
    mix_inputs = "[0:a]"
    for i, ts in enumerate(timestamps):
        delay_ms = int(ts * 1000)
        label = f"[sfx{i}]"
        filter_parts.append(f"[{i + 1}:a]adelay={delay_ms}|{delay_ms},volume=0.6{label}")
        mix_inputs += label

    n_inputs = 1 + len(timestamps)
    filter_parts.append(f"{mix_inputs}amix=inputs={n_inputs}:duration=first[aout]")
    filter_str = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(tmp_out),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        # Replace original with version that has sound effects
        import shutil
        shutil.move(str(tmp_out), str(video_path))
