import { useState } from "react";
import { uploadVideo, UploadResponse } from "../api/client";

type UploadState = "idle" | "uploading" | "done" | "error";

export function useUpload() {
  const [state, setState] = useState<UploadState>("idle");
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function upload(file: File) {
    setState("uploading");
    setError(null);
    try {
      const res = await uploadVideo(file);
      setResult(res);
      setState("done");
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Upload failed";
      setError(msg);
      setState("error");
    }
  }

  function reset() {
    setState("idle");
    setResult(null);
    setError(null);
  }

  return { state, result, error, upload, reset };
}
