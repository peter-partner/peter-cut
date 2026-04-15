"""
Detects scene/take voice cues in video audio using faster-whisper.

Supports:
  - English: "scene 1 take 1", "scene one take two"
  - Thai:    "ฉาก 1 เทค 1", "ฉากหนึ่ง เทคสอง"
"""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CuePoint:
    timestamp: float
    scene: int
    take: int
    raw_text: str


THAI_NUMBERS = {
    "หนึ่ง": 1, "สอง": 2, "สาม": 3, "สี่": 4, "ห้า": 5,
    "หก": 6, "เจ็ด": 7, "แปด": 8, "เก้า": 9, "สิบ": 10,
    "สิบเอ็ด": 11, "สิบสอง": 12, "สิบสาม": 13, "สิบสี่": 14, "สิบห้า": 15,
}

ENGLISH_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
}


def _word_to_int(word: str) -> int | None:
    word = word.strip()
    if word.isdigit():
        return int(word)
    w = word.lower()
    if w in ENGLISH_NUMBERS:
        return ENGLISH_NUMBERS[w]
    if word in THAI_NUMBERS:
        return THAI_NUMBERS[word]
    return None


def _parse_cue_from_text(text: str) -> tuple[int, int] | None:
    text_lower = text.lower().strip()

    en_match = re.search(r"scene\s+(\w+)\s+take\s+(\w+)", text_lower)
    if en_match:
        scene = _word_to_int(en_match.group(1))
        take = _word_to_int(en_match.group(2))
        if scene and take:
            return scene, take

    th_match = re.search(r"ฉาก\s*(\S+)\s*เทค\s*(\S+)", text)
    if th_match:
        scene = _word_to_int(th_match.group(1))
        take = _word_to_int(th_match.group(2))
        if scene and take:
            return scene, take

    for th_scene_word, scene_num in THAI_NUMBERS.items():
        for th_take_word, take_num in THAI_NUMBERS.items():
            if f"ฉาก{th_scene_word}" in text and f"เทค{th_take_word}" in text:
                return scene_num, take_num

    return None


class SpeechDetector:
    def __init__(self, model_name: str = "base"):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_name, compute_type="int8", device="cpu")

    def detect_cues(self, video_path: str | Path, language: str | None = None) -> list[CuePoint]:
        video_path = str(video_path)
        kwargs = {}
        if language:
            kwargs["language"] = language

        segments, _ = self.model.transcribe(video_path, **kwargs)

        cues: list[CuePoint] = []
        for seg in segments:
            parsed = _parse_cue_from_text(seg.text)
            if parsed:
                scene, take = parsed
                cues.append(CuePoint(
                    timestamp=seg.start,
                    scene=scene,
                    take=take,
                    raw_text=seg.text.strip(),
                ))

        cues.sort(key=lambda c: c.timestamp)
        return cues
