import React, { useState } from "react";
import { VideoUpload } from "./components/VideoUpload";
import { TransitionPicker } from "./components/TransitionPicker";
import { ProcessingStatus } from "./components/ProcessingStatus";
import { useUpload } from "./hooks/useUpload";
import { useProcessing } from "./hooks/useProcessing";
import { getExportUrl, ProcessRequest } from "./api/client";
import th from "./i18n/th";
import en from "./i18n/en";

const LANGS = { th, en } as const;

export default function App() {
  const [uiLang, setUiLang] = useState<"th" | "en">("th");
  const t = LANGS[uiLang];

  const [opts, setOpts] = useState<ProcessRequest>({
    transition_style: "viral_zoom",
    transition_sound: "whoosh",
    language: null,
  });

  const upload = useUpload();
  const processing = useProcessing();

  const jobId = upload.result?.job_id;
  const isProcessing = processing.status?.status === "processing" || processing.status?.status === "queued";
  const isDone = processing.status?.status === "done";

  async function handleProcess() {
    if (!jobId) return;
    await processing.startJob(jobId, opts);
  }

  function handleReset() {
    upload.reset();
    processing.reset();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-indigo-950 font-thai">
      {/* Header */}
      <header className="border-b border-white/10 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl">✂️</span>
          <span className="text-white font-bold text-xl tracking-tight">AutoCut</span>
          <span className="text-xs text-indigo-300 border border-indigo-700 rounded-full px-2 py-0.5">
            v0.1
          </span>
        </div>
        <div className="flex gap-2">
          {(["th", "en"] as const).map((lang) => (
            <button
              key={lang}
              onClick={() => setUiLang(lang)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition
                ${uiLang === lang ? "bg-indigo-600 text-white" : "text-gray-400 hover:text-white"}`}
            >
              {lang === "th" ? "🇹🇭 ไทย" : "🇬🇧 EN"}
            </button>
          ))}
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-12 space-y-8">
        {/* Hero */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-3">{t.tagline}</h1>
          <p className="text-indigo-300">{t.subtitle}</p>
        </div>

        {/* How to use */}
        <div className="bg-white/5 rounded-2xl p-6 text-sm text-indigo-200 space-y-1">
          <p className="font-semibold text-white mb-3">{t.howTitle}</p>
          <p>{t.howStep1}</p>
          <p>{t.howStep2}</p>
          <p>{t.howStep3}</p>
          <p>{t.howStep4}</p>
        </div>

        {/* Upload */}
        {!upload.result && (
          <VideoUpload
            t={t}
            onFile={upload.upload}
            uploading={upload.state === "uploading"}
          />
        )}

        {/* Upload error */}
        {upload.error && (
          <div className="bg-red-900/40 border border-red-700 rounded-xl p-4 text-red-300 text-sm">
            {t.errUpload}: {upload.error}
          </div>
        )}

        {/* After upload: settings + process */}
        {upload.result && !isDone && (
          <div className="bg-white rounded-2xl p-6 space-y-6">
            <div className="flex items-center gap-3 text-green-600">
              <span className="text-2xl">✅</span>
              <div>
                <p className="font-semibold">{t.uploadDone}</p>
                <p className="text-sm text-gray-500">{upload.result.filename} — {upload.result.size_mb} MB</p>
              </div>
            </div>

            <TransitionPicker t={t} opts={opts} onChange={setOpts} />

            {processing.status && (
              <ProcessingStatus t={t} status={processing.status} />
            )}

            {processing.error && !processing.status && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-600 text-sm">
                {processing.error}
              </div>
            )}

            {!isProcessing && (
              <button
                onClick={handleProcess}
                disabled={isProcessing}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold text-lg transition disabled:opacity-50"
              >
                {isProcessing ? t.processing : t.processBtn}
              </button>
            )}
          </div>
        )}

        {/* Done! */}
        {isDone && processing.status && (
          <div className="bg-white rounded-2xl p-6 space-y-5">
            <div className="text-center">
              <div className="text-5xl mb-3">🎉</div>
              <h2 className="text-2xl font-bold text-gray-800">{t.downloadReady}</h2>
            </div>

            <ProcessingStatus t={t} status={processing.status} />

            <div className="flex gap-3">
              <a
                href={getExportUrl(jobId!)}
                download
                className="flex-1 text-center py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl font-semibold transition"
              >
                ⬇️ {t.downloadBtn}
              </a>
              <button
                onClick={handleReset}
                className="px-5 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-medium transition"
              >
                + ใหม่
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
