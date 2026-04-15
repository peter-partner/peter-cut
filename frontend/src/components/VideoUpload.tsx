import React, { useRef, useState } from "react";
import type { Translations } from "../i18n/th";

interface Props {
  t: Translations;
  onFile: (file: File) => void;
  uploading: boolean;
}

export function VideoUpload({ t, onFile, uploading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    const file = files[0];
    if (!file.type.startsWith("video/")) {
      alert("กรุณาเลือกไฟล์วิดีโอ / Please select a video file");
      return;
    }
    onFile(file);
  }

  return (
    <div
      className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all
        ${dragging ? "border-indigo-500 bg-indigo-50" : "border-gray-300 hover:border-indigo-400 hover:bg-gray-50"}
        ${uploading ? "opacity-50 pointer-events-none" : ""}
      `}
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        handleFiles(e.dataTransfer.files);
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <div className="text-6xl mb-4">🎬</div>
      <p className="text-lg font-semibold text-gray-700 mb-2">
        {uploading ? t.uploading : t.uploadDrop}
      </p>
      <p className="text-sm text-gray-400">{t.uploadSupported}</p>
      {!uploading && (
        <button
          className="mt-6 px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition"
          onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
        >
          {t.uploadBtn}
        </button>
      )}
    </div>
  );
}
