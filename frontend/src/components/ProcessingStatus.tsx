import React from "react";
import type { StatusResponse, SceneInfo } from "../api/client";
import type { Translations } from "../i18n/th";

interface Props {
  t: Translations;
  status: StatusResponse;
}

export function ProcessingStatus({ t, status }: Props) {
  const isDone = status.status === "done";
  const isError = status.status === "error";

  return (
    <div className="space-y-4">
      {/* Progress bar */}
      <div>
        <div className="flex justify-between text-sm mb-1">
          <span className="text-gray-600">{status.message}</span>
          <span className="font-medium text-indigo-600">{status.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all duration-500 ${
              isError ? "bg-red-500" : isDone ? "bg-green-500" : "bg-indigo-500"
            }`}
            style={{ width: `${status.progress}%` }}
          />
        </div>
      </div>

      {/* Error */}
      {isError && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm">
          <strong>{t.error}:</strong> {status.error}
        </div>
      )}

      {/* Scene list */}
      {status.scenes && status.scenes.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-600 mb-2">
            {t.scenesFound}: {status.scenes.length} {t.scenes}
          </p>
          <div className="space-y-2">
            {status.scenes.map((scene: SceneInfo) => (
              <div
                key={scene.scene}
                className="flex items-center justify-between bg-white border border-gray-100 rounded-xl px-4 py-3 text-sm"
              >
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 bg-indigo-100 text-indigo-700 rounded-lg flex items-center justify-center font-bold text-xs">
                    {scene.scene}
                  </span>
                  <span className="text-gray-700">
                    ฉาก {scene.scene} — {t.take} {scene.best_take}
                  </span>
                </div>
                <span className="text-gray-400">{scene.duration.toFixed(1)}s</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
