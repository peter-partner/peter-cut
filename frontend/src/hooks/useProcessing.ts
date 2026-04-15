import { useState, useRef } from "react";
import { startProcessing, getStatus, ProcessRequest, StatusResponse } from "../api/client";

export function useProcessing() {
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  async function startJob(jobId: string, opts: ProcessRequest) {
    setError(null);
    setStatus(null);
    try {
      await startProcessing(jobId, opts);

      pollRef.current = setInterval(async () => {
        try {
          const s = await getStatus(jobId);
          setStatus(s);
          if (s.status === "done" || s.status === "error") {
            if (pollRef.current) clearInterval(pollRef.current);
            if (s.status === "error") setError(s.error || "Unknown error");
          }
        } catch {
          if (pollRef.current) clearInterval(pollRef.current);
          setError("Failed to poll job status");
        }
      }, 2000);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Failed to start processing";
      setError(msg);
    }
  }

  function reset() {
    if (pollRef.current) clearInterval(pollRef.current);
    setStatus(null);
    setError(null);
  }

  return { status, error, startJob, reset };
}
