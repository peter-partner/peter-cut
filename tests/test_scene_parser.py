"""Tests for scene plan builder — the take-selection logic."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from processors.speech_detector import CuePoint
from processors.scene_parser import build_scene_plan, CUE_OFFSET_SECONDS


def cues(*args):
    return [CuePoint(t, s, k, f"scene {s} take {k}") for t, s, k in args]


def test_single_take():
    plan = build_scene_plan(cues((0, 1, 1)), 60)
    assert len(plan.selected_clips) == 1
    assert plan.selected_clips[0].scene == 1


def test_last_take_wins():
    plan = build_scene_plan(cues((0, 1, 1), (30, 1, 2)), 60)
    assert len(plan.selected_clips) == 1
    assert plan.selected_clips[0].take == 2


def test_multi_scene():
    plan = build_scene_plan(cues((0, 1, 1), (30, 2, 1)), 60)
    assert [c.scene for c in plan.selected_clips] == [1, 2]


def test_complex():
    plan = build_scene_plan(cues(
        (0, 1, 1), (20, 1, 2),     # scene 1: keep take 2
        (40, 2, 1),                 # scene 2: keep take 1
        (60, 3, 1), (80, 3, 2), (100, 3, 3),  # scene 3: keep take 3
    ), 120)
    takes = {c.scene: c.take for c in plan.selected_clips}
    assert takes == {1: 2, 2: 1, 3: 3}


def test_empty():
    plan = build_scene_plan([], 60)
    assert plan.selected_clips == []


def test_offset_applied():
    plan = build_scene_plan(cues((5, 1, 1)), 60)
    assert plan.selected_clips[0].start == 5 + CUE_OFFSET_SECONDS


def test_scene_order_by_number():
    plan = build_scene_plan(cues((0, 2, 1), (30, 1, 1)), 60)
    assert [c.scene for c in plan.selected_clips] == [1, 2]
