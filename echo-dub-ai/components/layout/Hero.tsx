"use client";

import { motion } from "framer-motion";
import { Sparkles, Upload, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Hero() {
  function scrollToUpload() {
    document
      .getElementById("upload-section")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  }

  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-violet-50 via-pink-50 to-white">

      {/* Animated Background Blobs */}

      <motion.div
        animate={{
          x: [0, 40, 0],
          y: [0, 30, 0],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
        }}
        className="absolute -left-24 top-10 h-80 w-80 rounded-full bg-violet-300/40 blur-3xl"
      />

      <motion.div
        animate={{
          x: [0, -50, 0],
          y: [0, 20, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
        }}
        className="absolute right-0 top-20 h-[28rem] w-[28rem] rounded-full bg-pink-300/40 blur-3xl"
      />

      <div className="mx-auto flex max-w-7xl flex-col items-center px-6 py-28 text-center">

        <motion.div
          initial={{
            opacity: 0,
            y: 40,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.8,
          }}
        >

          {/* Badge */}

          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/40 bg-white/60 px-5 py-2 backdrop-blur-md shadow-lg">

            <Sparkles size={16} />

            <span className="font-medium text-violet-700">
              AI Powered Video Dubbing
            </span>

          </div>

          {/* Heading */}

          <h1 className="text-5xl font-black leading-tight text-slate-900 md:text-7xl">

            Dub Videos Into

            <br />

            <span className="bg-gradient-to-r from-violet-600 via-fuchsia-500 to-pink-500 bg-clip-text text-transparent">

              Any Language

            </span>

          </h1>

          {/* Description */}

          <p className="mx-auto mt-8 max-w-3xl text-lg leading-8 text-slate-600 md:text-xl">

            Experience seamless AI-powered video dubbing with
            natural voice synthesis, intelligent translation,
            speaker-aware processing, and perfectly synchronized
            audio—all in one modern platform.

          </p>

          {/* Buttons */}

          <div className="mt-12 flex flex-wrap justify-center gap-4">

            <Button
              size="lg"
              onClick={scrollToUpload}
              className="rounded-2xl bg-violet-600 px-8 py-6 text-base shadow-lg transition hover:scale-105 hover:bg-violet-700"
            >
              <Upload className="mr-2 h-5 w-5" />

              Start Dubbing

            </Button>

            <Button
              size="lg"
              variant="outline"
              className="rounded-2xl border-violet-200 bg-white/70 px-8 py-6 text-base backdrop-blur hover:bg-white"
            >
              <Cpu className="mr-2 h-5 w-5" />

              FastAPI • Gemini AI

            </Button>

          </div>

        </motion.div>

      </div>

    </section>
  );
}