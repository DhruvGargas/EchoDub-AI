"use client";

import { Download, Loader2, CheckCircle2 } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

interface ProgressCardProps {
  progress: number;
  status: string;
  step: string;
  downloadUrl?: string;
}

export default function ProgressCard({
  progress,
  status,
  step,
  downloadUrl,
}: ProgressCardProps) {
  const completed = status === "completed";

  return (
    <section className="mx-auto mt-10 mb-20 max-w-4xl px-6">
      <div className="rounded-3xl bg-white p-10 shadow-xl">

        <div className="flex items-center justify-between">

          <div>
            <h2 className="text-3xl font-bold text-slate-800">
              Processing Video
            </h2>

            <p className="mt-2 text-slate-500">
              {completed
                ? "Your dubbed video is ready!"
                : "AI is processing your video..."}
            </p>
          </div>

          {completed ? (
            <CheckCircle2
              size={48}
              className="text-green-500"
            />
          ) : (
            <Loader2
              size={42}
              className="animate-spin text-violet-500"
            />
          )}

        </div>

        <div className="mt-10">

          <div className="mb-3 flex justify-between">

            <span className="font-semibold text-violet-600">
              {step}
            </span>

            <span className="font-bold text-slate-800">
              {progress}%
            </span>

          </div>

          <Progress value={progress} className="h-3" />

        </div>

        {completed && downloadUrl && (

          <div className="mt-10 flex justify-center">

            <Button
              size="lg"
              className="rounded-2xl bg-green-500 hover:bg-green-600"
              onClick={() => {
                window.open(downloadUrl, "_blank");
              }}
            >
              <Download className="mr-2 h-5 w-5" />
              Download Dubbed Video
            </Button>

          </div>

        )}

      </div>
    </section>
  );
}