"""Tests for voice cue parsing — the core detection logic."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from processors.speech_detector import _parse_cue_from_text


# English
def test_english_digits():
    assert _parse_cue_from_text("scene 1 take 2") == (1, 2)

def test_english_words():
    assert _parse_cue_from_text("scene one take three") == (1, 3)

def test_english_in_sentence():
    assert _parse_cue_from_text("ok everyone, scene 4 take 2, action") == (4, 2)

# Thai
def test_thai_digits():
    assert _parse_cue_from_text("ฉาก 1 เทค 1") == (1, 1)

def test_thai_number_words():
    assert _parse_cue_from_text("ฉากหนึ่ง เทคสอง") == (1, 2)

def test_thai_spaced():
    assert _parse_cue_from_text("ฉาก 5 เทค 3") == (5, 3)

# No cue
def test_no_cue():
    assert _parse_cue_from_text("hello world") is None

def test_empty():
    assert _parse_cue_from_text("") is None

def test_partial():
    assert _parse_cue_from_text("scene 1") is None
