"use client";

import { useState } from "react";

import Navbar from "@/components/layout/Navbar";
import Hero from "@/components/layout/Hero";
import UploadCard from "@/components/upload/UploadCard";
import ProgressCard from "@/components/progress/ProgressCard";

import { useJobStatus } from "@/hooks/useJobStatus";
import { getDownloadUrl } from "@/services/api";

export default function Home() {
  const [jobId, setJobId] = useState<number | null>(null);

  const job = useJobStatus(jobId);

  return (
    <>
      <Navbar />

      <main className="pt-28">

        <Hero />

        <UploadCard
          onUploadSuccess={(id) => setJobId(id)}
        />

        {job && (
          <ProgressCard
            progress={job.progress}
            status={job.status}
            step={job.current_step}
            downloadUrl={
              job.status === "completed"
                ? getDownloadUrl(String(job.id))
                : undefined
            }
          />
        )}

      </main>
    </>
  );
}