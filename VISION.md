# VISION — AutoCut Platform

## Core Problem

Video production is time-consuming. Even a simple 10-minute final video may require hours of raw footage with multiple takes per scene. Editors spend the majority of their time just finding the right takes and making basic cuts — work that a machine can do.

## The Vision

AutoCut removes the most tedious part of video editing: **identifying and isolating the correct takes**. Directors already say which scene and take they're filming out loud. AutoCut simply listens.

The result: raw footage goes in → final cut comes out.

## Target User

- **Phase 1 (MVP):** Thai content creators, YouTubers, short-film directors
- **Phase 2:** Southeast Asian market expansion
- **Phase 3:** Global platform with multi-language support

## Editing Intelligence

### Take Selection Logic

```
For each recorded clip:
  1. Detect voice cue: "Scene X Take Y"
  2. Record timestamp of cue
  3. After all cues are detected, group by Scene number
  4. For each scene, select the clip with the HIGHEST take number
     (= the last recorded take = director's final choice)
  5. Discard all lower-numbered takes for that scene
```

Example:
```
Raw footage timeline:
  00:00 — "Scene 1 Take 1" → footage...
  02:30 — "Scene 1 Take 2" → footage...  ← KEEP THIS
  05:00 — "Scene 2 Take 1" → footage...  ← KEEP THIS
  07:00 — "Scene 3 Take 1" → footage...
  09:30 — "Scene 3 Take 2" → footage...
  12:00 — "Scene 3 Take 3" → footage...  ← KEEP THIS

Output:
  Scene 1 (Take 2) → [transition] → Scene 2 (Take 1) → [transition] → Scene 3 (Take 3)
```

## Transition Effects

### Zoom In
- Gradually zooms into the center of the frame during cut
- Duration: 0.3–0.8 seconds
- Use: Documentary feel, emphasis

### Zoom Out
- Pulls back from the subject
- Duration: 0.3–0.8 seconds
- Use: Reveal, establishing shot

### Distorted Viral Zoom
- Rapid zoom combined with chromatic aberration distortion
- Duration: 0.1–0.3 seconds
- Use: Social media / TikTok / viral content style
- Sound: Bass-heavy whoosh

### Fade
- Classic cross-fade
- Duration: 0.5–1.0 seconds
- Use: Time passage, emotional scenes

### Hard Cut
- Instant cut with no transition
- Duration: 0 seconds
- Use: Action, dialogue

## Sound Design

Each transition can optionally include a sound effect:
- **Whoosh** — classic fast camera movement sound
- **Swoosh** — lighter, more subtle
- **Viral Zoom** — deep bass punch + distortion
- **Impact** — slam/thud for hard cuts
- **Silence** — no sound

## Language Support

AutoCut v1 supports:
- **Thai (ภาษาไทย)** — primary market
- **English** — secondary

Voice cue detection uses OpenAI Whisper which natively supports both languages. The Whisper model will transcribe and the scene parser handles both:
- English: "scene one take two", "scene 1 take 2"
- Thai: "ฉาก 1 เทค 1", "ฉากหนึ่ง เทคสอง"

## Roadmap

### v0.1 — Foundation
- [ ] Project scaffold (backend + frontend)
- [ ] Video upload API
- [ ] Basic Whisper integration
- [ ] Scene/take cue detection (English)
- [ ] Simple cut-only editing (no transitions)
- [ ] Video export

### v0.2 — Thai Language
- [ ] Thai voice cue detection
- [ ] Thai UI
- [ ] Thai number word recognition (หนึ่ง, สอง, สาม...)

### v0.3 — Transitions
- [ ] Zoom In / Zoom Out transitions
- [ ] Viral Zoom effect
- [ ] Fade transition
- [ ] Transition sound effects

### v0.4 — UX Polish
- [ ] Real-time processing progress
- [ ] Scene preview before export
- [ ] Transition picker per scene
- [ ] Manual override (keep/discard specific takes)

### v1.0 — Production
- [ ] Docker deployment
- [ ] Cloud storage (S3)
- [ ] User authentication
- [ ] Processing history
- [ ] Batch processing

### v2.0 — Platform
- [ ] Mobile app (React Native)
- [ ] Auto color grading
- [ ] AI-based quality scoring (which take is technically best)
- [ ] Music/background audio sync
- [ ] Subtitle generation (Thai + English)
