"use client";

import { useEffect, useState } from "react";
import { Sparkles, Rocket, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const [showNavbar, setShowNavbar] = useState(true);

  useEffect(() => {
    let lastScrollY = window.scrollY;

    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      // Always show at the very top
      if (currentScrollY < 50) {
        setShowNavbar(true);
      } else if (currentScrollY > lastScrollY) {
        // Scrolling down
        setShowNavbar(false);
      } else {
        // Scrolling up
        setShowNavbar(true);
      }

      lastScrollY = currentScrollY;
    };

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  function scrollToUpload() {
    document
      .getElementById("upload-section")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  }

  function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 px-4 pt-4 transition-all duration-500 ${
        showNavbar
          ? "translate-y-0 opacity-100"
          : "-translate-y-28 opacity-0"
      }`}
    >
      <nav className="mx-auto flex h-20 max-w-7xl items-center justify-between rounded-3xl border border-white/50 bg-white/70 px-8 shadow-xl backdrop-blur-xl">

        {/* Logo */}
        <div className="flex items-center gap-4">
          <div className="rounded-2xl bg-gradient-to-br from-violet-500 to-pink-500 p-3 shadow-lg">
            <Sparkles className="h-6 w-6 text-white" />
          </div>

          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-800">
              EchoDub AI
            </h1>

            <p className="text-xs text-slate-500">
              AI Video Dubbing Platform
            </p>
          </div>
        </div>

        {/* Navigation */}
        <div className="hidden items-center gap-8 md:flex">

          <button
            onClick={scrollToTop}
            className="text-sm font-medium text-slate-600 transition hover:text-violet-600"
          >
            Home
          </button>

          <button
            onClick={scrollToUpload}
            className="text-sm font-medium text-slate-600 transition hover:text-violet-600"
          >
            Upload
          </button>

          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium text-slate-600 transition hover:text-violet-600"
          >
            API Docs
          </a>

        </div>

        {/* Buttons */}
        <div className="flex items-center gap-3">

          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden md:block"
          >
            <Button
              variant="outline"
              className="rounded-2xl"
            >
              <BookOpen className="mr-2 h-4 w-4" />
              Swagger
            </Button>
          </a>

          <Button
            onClick={scrollToUpload}
            className="rounded-2xl bg-gradient-to-r from-violet-600 to-pink-500 shadow-lg transition-all duration-300 hover:scale-105 hover:from-violet-700 hover:to-pink-600"
          >
            <Rocket className="mr-2 h-4 w-4" />
            Start Dubbing
          </Button>

        </div>

      </nav>
    </header>
  );
}