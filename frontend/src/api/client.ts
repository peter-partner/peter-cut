import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export interface UploadResponse {
  job_id: string;
  filename: string;
  size_mb: number;
  message: string;
}

export interface ProcessRequest {
  transition_style: "cut" | "fade" | "zoom_in" | "zoom_out" | "viral_zoom";
  transition_sound: "whoosh" | "swoosh" | "viral_zoom" | "impact" | "none";
  language: "th" | "en" | null;
}

export interface SceneInfo {
  scene: number;
  best_take: number;
  start: number;
  end: number;
  duration: number;
}

export interface StatusResponse {
  job_id: string;
  status: "queued" | "processing" | "done" | "error";
  progress: number;
  message: string;
  scenes: SceneInfo[] | null;
  error: string | null;
}

export async function uploadVideo(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append("video", file);
  const res = await api.post<UploadResponse>("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function startProcessing(
  jobId: string,
  opts: ProcessRequest
): Promise<void> {
  await api.post(`/process/${jobId}`, opts);
}

export async function getStatus(jobId: string): Promise<StatusResponse> {
  const res = await api.get<StatusResponse>(`/status/${jobId}`);
  return res.data;
}

export function getExportUrl(jobId: string): string {
  return `/api/export/${jobId}`;
}
