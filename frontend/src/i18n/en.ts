import type { Translations } from "./th";

const en: Translations = {
  appName: "AutoCut",
  tagline: "AI-Powered Automatic Video Editing",
  subtitle: "Upload your raw footage — AutoCut handles the rest.",

  uploadTitle: "Upload Video",
  uploadDrop: "Drag & drop your video here, or click to select",
  uploadSupported: "Supported: MP4, MOV, AVI, MKV (up to 2GB)",
  uploadBtn: "Choose Video",
  uploading: "Uploading...",
  uploadDone: "Upload successful!",

  settingsTitle: "Edit Settings",
  transitionStyle: "Transition Style",
  transitionSound: "Transition Sound",
  language: "Video Language",
  langAuto: "Auto-detect",
  langThai: "Thai",
  langEnglish: "English",

  transitionCut: "Hard Cut",
  transitionFade: "Fade",
  transitionZoomIn: "Zoom In",
  transitionZoomOut: "Zoom Out",
  transitionViralZoom: "Viral Zoom (TikTok)",

  soundWhoosh: "Whoosh",
  soundSwoosh: "Swoosh",
  soundViralZoom: "Viral Zoom",
  soundImpact: "Impact",
  soundNone: "No Sound",

  processBtn: "Start Editing",
  processing: "Processing...",
  processingStep: "Processing",
  detecting: "Analysing audio...",
  cutting: "Cutting scenes...",
  exporting: "Exporting video...",

  done: "Done!",
  error: "Error",
  scenesFound: "Scenes found",
  scenes: "scenes",
  take: "Take",

  downloadBtn: "Download Video",
  downloadReady: "Your video is ready!",

  howTitle: "How to Use",
  howStep1: '1. Record your footage by saying "Scene 1 Take 1" before each shot',
  howStep2: "2. Upload the raw video",
  howStep3: "3. AutoCut automatically selects the best take for each scene",
  howStep4: "4. Download your edited video",

  errUpload: "Upload failed. Please try again.",
  errProcess: "Processing failed.",
  errNoCues:
    "No scene/take cues detected. Make sure to say 'Scene X Take Y' before each shot.",
};

export default en;
