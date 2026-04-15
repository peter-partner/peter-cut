const th = {
  appName: "AutoCut",
  tagline: "ตัดต่อวิดีโออัตโนมัติด้วย AI",
  subtitle: "อัปโหลดวิดีโอดิบของคุณ — AutoCut จะจัดการส่วนที่เหลือทั้งหมด",

  // Upload
  uploadTitle: "อัปโหลดวิดีโอ",
  uploadDrop: "ลากและวางวิดีโอที่นี่ หรือคลิกเพื่อเลือกไฟล์",
  uploadSupported: "รองรับ: MP4, MOV, AVI, MKV (ไม่เกิน 2GB)",
  uploadBtn: "เลือกวิดีโอ",
  uploading: "กำลังอัปโหลด...",
  uploadDone: "อัปโหลดสำเร็จ!",

  // Settings
  settingsTitle: "ตั้งค่าการตัดต่อ",
  transitionStyle: "สไตล์การเปลี่ยนฉาก",
  transitionSound: "เสียงเอฟเฟกต์",
  language: "ภาษาในวิดีโอ",
  langAuto: "อัตโนมัติ",
  langThai: "ภาษาไทย",
  langEnglish: "ภาษาอังกฤษ",

  // Transitions
  transitionCut: "ตัดตรง",
  transitionFade: "เฟด",
  transitionZoomIn: "ซูมเข้า",
  transitionZoomOut: "ซูมออก",
  transitionViralZoom: "Viral Zoom (TikTok)",

  // Sounds
  soundWhoosh: "Whoosh",
  soundSwoosh: "Swoosh",
  soundViralZoom: "Viral Zoom",
  soundImpact: "Impact",
  soundNone: "ไม่มีเสียง",

  // Processing
  processBtn: "เริ่มตัดต่อ",
  processing: "กำลังตัดต่อ...",
  processingStep: "กำลังดำเนินการ",
  detecting: "กำลังวิเคราะห์เสียง...",
  cutting: "กำลังตัดต่อฉาก...",
  exporting: "กำลัง export วิดีโอ...",

  // Status
  done: "เสร็จสิ้น!",
  error: "เกิดข้อผิดพลาด",
  scenesFound: "พบฉากทั้งหมด",
  scenes: "ฉาก",
  take: "เทค",

  // Export
  downloadBtn: "ดาวน์โหลดวิดีโอ",
  downloadReady: "วิดีโอของคุณพร้อมแล้ว!",

  // Instructions
  howTitle: "วิธีใช้งาน",
  howStep1: "1. บันทึกวิดีโอของคุณโดยพูด \"ฉาก 1 เทค 1\" ก่อนเริ่มถ่าย",
  howStep2: "2. อัปโหลดวิดีโอดิบ",
  howStep3: "3. AutoCut จะเลือกเทคล่าสุดของแต่ละฉากโดยอัตโนมัติ",
  howStep4: "4. ดาวน์โหลดวิดีโอที่ตัดต่อแล้ว",

  // Errors
  errUpload: "อัปโหลดล้มเหลว กรุณาลองใหม่",
  errProcess: "ประมวลผลล้มเหลว",
  errNoCues: "ไม่พบสัญญาณ scene/take ในวิดีโอ กรุณาตรวจสอบว่าพูดคำสั่งก่อนถ่ายทุกฉาก",
};

export default th;
export type Translations = typeof th;
