"use client";

import { useRef, useState } from "react";
import { Upload, Video, Loader2 } from "lucide-react";

import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { uploadVideo } from "@/services/api";

interface UploadCardProps {
  onUploadSuccess: (jobId: number) => void;
}

export default function UploadCard({
  onUploadSuccess,
}: UploadCardProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("Hindi");
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState<number | null>(null);
  const [message, setMessage] = useState("");

  function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);
  }

  async function handleUpload() {
    if (!selectedFile) {
      alert("Please select a video first.");
      return;
    }

    try {
      setLoading(true);

      const data = await uploadVideo(
        selectedFile,
        language
      );

      setJobId(data.job_id);
      setMessage(data.message);
      onUploadSuccess(data.job_id);
    } catch (error) {
  console.error(error);

  if (error instanceof Error) {
    alert(error.message);
  } else {
    alert("Upload failed.");
  }
} finally {
      setLoading(false);
    }
  }

  return (
    <section
  id="upload-section"
  className="mx-auto -mt-8 max-w-4xl px-6 pb-20"
>

      <Card className="relative overflow-hidden rounded-[32px] border border-white/60 bg-white/75 p-10 shadow-2xl backdrop-blur-xl transition-all duration-500 hover:-translate-y-1 hover:shadow-violet-200/60">
      <div className="absolute -right-24 -top-24 h-64 w-64 rounded-full bg-violet-200/30 blur-3xl" />

<div className="absolute -left-20 bottom-0 h-56 w-56 rounded-full bg-pink-200/30 blur-3xl" />
        <div className="flex flex-col items-center">

          <div className="mb-8 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 p-5 shadow-lg">
            <Upload className="h-10 w-10 text-white" />
          </div>

          <h2 className="text-3xl font-bold text-slate-800">
            Upload Your Video
          </h2>

          <p className="mt-3 text-center text-slate-500">
            Drag & drop your video here or browse from your computer.
          </p>

          <div
            onClick={() => inputRef.current?.click()}
            className="mt-10 flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-[28px] border-2 border-dashed border-violet-300 bg-gradient-to-br from-violet-50 to-pink-50 transition-all duration-300 hover:scale-[1.01] hover:border-violet-500 hover:shadow-xl"
          >
            <Video className="mb-5 h-16 w-16 text-violet-500" />

            <p className="font-medium text-slate-700">
              Click to browse your video
            </p>

            <p className="mt-2 text-sm text-slate-500">
              MP4 • Maximum 10 minutes
            </p>

            <input
              ref={inputRef}
              type="file"
              accept="video/mp4"
              hidden
              onChange={handleFileChange}
            />
          </div>

          {selectedFile && (
  <div className="mt-6 w-full rounded-3xl border border-violet-100 bg-violet-50/70 p-6">

    <h3 className="font-semibold text-violet-700">
      Selected File
    </h3>

    <p className="mt-3 text-slate-700 font-medium">
      {selectedFile.name}
    </p>

    <p className="mt-2 text-sm text-slate-500">
      {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
    </p>

  </div>
)}

          <div className="mt-6 w-full">

            <label className="mb-2 block text-sm font-medium text-slate-700">
              Target Language
            </label>

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full rounded-2xl border border-violet-200 p-3 outline-none focus:ring-2 focus:ring-violet-400"
            >
              <option>Hindi</option>
              <option>English</option>
              <option>Spanish</option>
              <option>French</option>
              <option>German</option>
              <option>Japanese</option>
            </select>

          </div>

          <Button
            onClick={handleUpload}
            disabled={loading}
            className="mt-8 rounded-2xl bg-gradient-to-r from-violet-600 to-pink-500 px-12 py-6 text-base shadow-lg transition-all duration-300 hover:scale-105 hover:from-violet-700 hover:to-pink-600"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Uploading...
              </>
            ) : (
              <>✨ Start Dubbing</>
            )}
          </Button>

          {jobId && (
            <div className="mt-8 w-full rounded-3xl border border-green-200 bg-gradient-to-r from-green-50 to-emerald-50 p-6 text-center shadow-md">

              <h3 className="text-lg font-semibold text-green-700">
                Upload Successful 🎉
              </h3>

              <p className="mt-2 text-slate-700">
                {message}
              </p>

              <p className="mt-1 text-sm text-slate-500">
                Job ID: {jobId}
              </p>

            </div>
          )}

        </div>

      </Card>

    </section>
  );
}