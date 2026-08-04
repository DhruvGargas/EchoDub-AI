"use client";

import { useEffect, useState } from "react";
import { getJobStatus } from "@/services/api";
import { JobStatus } from "@/types/job";

export function useJobStatus(jobId: number | null) {
const [job, setJob] = useState<JobStatus | null>(null);

  useEffect(() => {
    if (!jobId) return;

    async function fetchStatus() {
      try {
        const data = await getJobStatus(jobId!.toString());
        setJob(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchStatus();

    const interval = setInterval(fetchStatus, 2000);

    return () => clearInterval(interval);

  }, [jobId]);

  return job;
}