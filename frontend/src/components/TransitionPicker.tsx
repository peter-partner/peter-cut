import React from "react";
import type { ProcessRequest } from "../api/client";
import type { Translations } from "../i18n/th";

interface Props {
  t: Translations;
  opts: ProcessRequest;
  onChange: (opts: ProcessRequest) => void;
}

const TRANSITIONS: { value: ProcessRequest["transition_style"]; labelKey: keyof Translations }[] = [
  { value: "viral_zoom", labelKey: "transitionViralZoom" },
  { value: "zoom_in", labelKey: "transitionZoomIn" },
  { value: "zoom_out", labelKey: "transitionZoomOut" },
  { value: "fade", labelKey: "transitionFade" },
  { value: "cut", labelKey: "transitionCut" },
];

const SOUNDS: { value: ProcessRequest["transition_sound"]; labelKey: keyof Translations }[] = [
  { value: "whoosh", labelKey: "soundWhoosh" },
  { value: "swoosh", labelKey: "soundSwoosh" },
  { value: "viral_zoom", labelKey: "soundViralZoom" },
  { value: "impact", labelKey: "soundImpact" },
  { value: "none", labelKey: "soundNone" },
];

const LANGUAGES: { value: ProcessRequest["language"]; labelKey: keyof Translations }[] = [
  { value: null, labelKey: "langAuto" },
  { value: "th", labelKey: "langThai" },
  { value: "en", labelKey: "langEnglish" },
];

export function TransitionPicker({ t, opts, onChange }: Props) {
  return (
    <div className="bg-gray-50 rounded-2xl p-6 space-y-5">
      <h3 className="font-semibold text-gray-700">{t.settingsTitle}</h3>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">{t.transitionStyle}</label>
        <div className="flex flex-wrap gap-2">
          {TRANSITIONS.map(({ value, labelKey }) => (
            <button
              key={value}
              onClick={() => onChange({ ...opts, transition_style: value })}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition
                ${opts.transition_style === value
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white text-gray-600 border-gray-300 hover:border-indigo-400"
                }`}
            >
              {t[labelKey] as string}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">{t.transitionSound}</label>
        <div className="flex flex-wrap gap-2">
          {SOUNDS.map(({ value, labelKey }) => (
            <button
              key={value}
              onClick={() => onChange({ ...opts, transition_sound: value })}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition
                ${opts.transition_sound === value
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white text-gray-600 border-gray-300 hover:border-indigo-400"
                }`}
            >
              {t[labelKey] as string}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">{t.language}</label>
        <div className="flex flex-wrap gap-2">
          {LANGUAGES.map(({ value, labelKey }) => (
            <button
              key={String(value)}
              onClick={() => onChange({ ...opts, language: value })}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition
                ${opts.language === value
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white text-gray-600 border-gray-300 hover:border-indigo-400"
                }`}
            >
              {t[labelKey] as string}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
