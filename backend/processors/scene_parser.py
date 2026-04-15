"""
Parses detected CuePoints into a structured scene plan.

Given cue points from the speech detector and the total video duration,
this module determines:
  - The start/end timestamps for each take of each scene
  - Which take to keep for each scene (always the last recorded take)
  - The final ordered list of clips to include in the edit
"""

from dataclasses import dataclass
from .speech_detector import CuePoint


@dataclass
class TakeClip:
    scene: int
    take: int
    start: float    # seconds — when this take begins (right after cue word)
    end: float      # seconds — when this take ends (when next cue starts, or video end)
    duration: float
    is_selected: bool  # True if this is the take to keep


@dataclass
class ScenePlan:
    """The full edit plan derived from all detected cues."""
    clips: list[TakeClip]          # All clips (selected and discarded)
    selected_clips: list[TakeClip] # Only the clips to include, in scene order

    def summary(self) -> str:
        lines = ["Edit Plan:"]
        by_scene: dict[int, list[TakeClip]] = {}
        for clip in self.clips:
            by_scene.setdefault(clip.scene, []).append(clip)

        for scene_num in sorted(by_scene):
            takes = by_scene[scene_num]
            for clip in takes:
                marker = "✓ KEEP" if clip.is_selected else "✗ skip"
                lines.append(
                    f"  Scene {clip.scene} Take {clip.take} "
                    f"[{clip.start:.1f}s – {clip.end:.1f}s] ({clip.duration:.1f}s)  {marker}"
                )
        total = sum(c.duration for c in self.selected_clips)
        lines.append(f"\nFinal edit: {len(self.selected_clips)} scene(s), {total:.1f}s total")
        return "\n".join(lines)


# Seconds to add after a cue word before the actual scene content starts.
# Accounts for the director finishing speaking "Scene 1 Take 1" before action.
CUE_OFFSET_SECONDS = 2.0


def build_scene_plan(cues: list[CuePoint], video_duration: float) -> ScenePlan:
    """
    Convert a list of CuePoints into a ScenePlan.

    Args:
        cues:           Sorted list of CuePoints from SpeechDetector.
        video_duration: Total duration of the source video in seconds.

    Returns:
        ScenePlan with all clips tagged and the selected_clips list ready for editing.
    """
    if not cues:
        return ScenePlan(clips=[], selected_clips=[])

    all_clips: list[TakeClip] = []

    for i, cue in enumerate(cues):
        clip_start = cue.timestamp + CUE_OFFSET_SECONDS
        clip_end = cues[i + 1].timestamp if i + 1 < len(cues) else video_duration

        # Skip degenerate clips (cue too close to next cue)
        if clip_end <= clip_start:
            clip_end = clip_start + 0.1

        all_clips.append(TakeClip(
            scene=cue.scene,
            take=cue.take,
            start=clip_start,
            end=clip_end,
            duration=clip_end - clip_start,
            is_selected=False,  # Will be set below
        ))

    # For each scene, mark only the highest take number as selected
    by_scene: dict[int, list[TakeClip]] = {}
    for clip in all_clips:
        by_scene.setdefault(clip.scene, []).append(clip)

    for scene_clips in by_scene.values():
        best = max(scene_clips, key=lambda c: c.take)
        best.is_selected = True

    selected = [c for c in all_clips if c.is_selected]
    selected.sort(key=lambda c: c.scene)

    plan = ScenePlan(clips=all_clips, selected_clips=selected)
    print(plan.summary())
    return plan
