"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Scissors,
  Play,
  AudioWaveform,
  FileText,
  Shield,
  Check,
  ArrowDown,
  Twitter,
  Github,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden bg-background">
      {/* Header */}
      <header className="flex items-center justify-between whitespace-nowrap border-b border-border px-6 lg:px-40 py-4 bg-background/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3 text-foreground">
          <div className="size-8 text-primary">
            <Scissors className="h-8 w-8" />
          </div>
          <h2 className="text-lg font-bold leading-tight tracking-[-0.015em]">ClipFlow</h2>
        </div>
        <div className="hidden md:flex items-center gap-8">
          <div className="flex items-center gap-6">
            <a
              className="text-foreground text-sm font-medium hover:text-primary transition-colors"
              href="#features"
            >
              Features
            </a>
            <a
              className="text-foreground text-sm font-medium hover:text-primary transition-colors"
              href="#privacy"
            >
              Privacy
            </a>
            {/* <a
              className="text-foreground text-sm font-medium hover:text-primary transition-colors"
              href="#pricing"
            >
              Pricing
            </a> */}
          </div>
          <div className="flex gap-3">
            <Link href="/login">
              <Button variant="outline" size="sm">
                Log In
              </Button>
            </Link>
            <Link href="/register">
              <Button size="sm">Sign Up</Button>
            </Link>
          </div>
        </div>
        <div className="md:hidden text-foreground">
          <span className="material-symbols-outlined">menu</span>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center px-6 lg:px-40 pt-16 pb-20 overflow-hidden relative">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary/20 blur-[120px] rounded-full pointer-events-none -z-10" />
        <div className="flex flex-col items-center max-w-[960px] text-center gap-8">
          <div className="flex flex-col gap-4">
            {/* <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-wide w-fit mx-auto">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              v2.0 Now Available
            </div> */}
            <h1 className="text-4xl md:text-6xl font-black leading-tight tracking-[-0.033em] text-foreground">
              Cut the Noise, <span className="text-primary">Keep the Privacy.</span>
            </h1>
            <p className="text-muted-foreground text-lg md:text-xl font-normal leading-relaxed max-w-[720px] mx-auto">
              Automatically remove silences and filler words in seconds. 100% local processing
              ensures your footage never leaves your device.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/register">
              <Button size="lg" className="shadow-lg shadow-primary/25">
                Start Editing for Free
              </Button>
            </Link>
            <Button
              variant="outline"
              size="lg"
              onClick={() => {
                const videoElement = document.getElementById('demo-video') as HTMLVideoElement;
                if (videoElement) {
                  videoElement.scrollIntoView({ behavior: 'smooth' });
                  videoElement.play().catch(console.error);
                }
              }}
            >
              <Play className="h-5 w-5 mr-2" />
              Watch Demo
            </Button>
          </div>
          {/* <div className="flex items-center gap-6 mt-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Check className="h-4 w-4 text-primary" />
              <span>No Cloud Upload</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="h-4 w-4 text-primary" />
              <span>Works Offline</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="h-4 w-4 text-primary" />
              <span>Mac & Windows</span>
            </div>
          </div> */}

          {/* App Preview */}
          <div className="mt-12 w-full relative group">
            <div className="absolute inset-0 bg-primary/20 blur-xl rounded-xl -z-10 group-hover:bg-primary/30 transition-all duration-500" />
            <div className="w-full bg-card rounded-xl border border-border shadow-2xl overflow-hidden aspect-video relative">
              <div className="absolute inset-0 flex flex-col">
                <div className="h-10 bg-muted border-b border-border flex items-center px-4 gap-2">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-destructive" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500" />
                    <div className="w-3 h-3 rounded-full bg-primary" />
                  </div>
                  <div className="flex-1 text-center text-xs text-muted-foreground font-mono">
                    ClipFlow Project - timeline_final.clip
                  </div>
                </div>
                <div className="flex-1 flex bg-background relative items-center justify-center">
                  <video
                    id="demo-video"
                    className="w-full h-full object-contain rounded-lg"
                    controls
                    preload="metadata"
                    poster="/thumbnail.png"
                  >
                    {/* <source src="/clipflow_demo.mp4" type="video/mp4" /> */}
                    <source src="/clipflow_demo.webm" type="video/webm" />
                    Your browser does not support the video tag.
                  </video>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section
        className="py-20 px-6 lg:px-40 bg-card border-y border-border"
        id="features"
      >
        <div className="max-w-[960px] mx-auto flex flex-col gap-16">
          <div className="text-center max-w-[720px] mx-auto">
            <h2 className="text-3xl md:text-4xl font-black leading-tight mb-4 text-foreground">
              AI-Powered Editing, <span className="text-primary">Maximum Privacy</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              Experience the speed of AI without compromising your footage security. We built
              ClipFlow to be the fastest way to edit dialogue.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col gap-4 rounded-xl border border-border bg-background p-6 hover:border-primary/50 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                <AudioWaveform className="h-7 w-7" />
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-bold text-foreground">Smart Silence Removal</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Automatically detect and cut silent pauses in seconds. Adjust threshold and
                  padding to keep it natural.
                </p>
              </div>
            </div>
            <div className="flex flex-col gap-4 rounded-xl border border-border bg-background p-6 hover:border-primary/50 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                <FileText className="h-7 w-7" />
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-bold text-foreground">Filter Word Detection</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Automatically identify and remove filler words like &quot;um,&quot; &quot;uh,&quot; and &quot;like&quot; from your transcript with a single click.
                </p>
              </div>
            </div>
            <div className="flex flex-col gap-4 rounded-xl border border-border bg-background p-6 hover:border-primary/50 transition-colors group">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                <Shield className="h-7 w-7" />
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-xl font-bold text-foreground">Hybrid Privacy Architecture</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  Best of both worlds: AI transcription on secure servers, editing magic happens locally. Your creative decisions stay on your device.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6 lg:px-40 bg-background" id="privacy">
        <div className="max-w-[960px] mx-auto">
          <div className="flex flex-col md:flex-row gap-12 items-center">
            <div className="flex-1 flex flex-col gap-6">
              <h2 className="text-3xl font-black leading-tight text-foreground">
                From 2 hours of raw footage to a polished cut in minutes.
              </h2>
              <p className="text-muted-foreground">
                Stop scrubbing through hours of silence and profanity. Let our AI identify the good takes,
                remove the dead air, and automatically filter unwanted words instantly.
              </p>
              <ul className="flex flex-col gap-4 mt-2">
                <li className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-primary" />
                  <span className="text-foreground font-medium">Auto-ripple deletes</span>
                </li>
                <li className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-primary" />
                  <span className="text-foreground font-medium">Export to MP4, MOV, or WebM formats</span>
                </li>
                <li className="flex items-center gap-3">
                  <Check className="h-5 w-5 text-primary" />
                  <span className="text-foreground font-medium">Customizable safety padding</span>
                </li>
              </ul>
            </div>
            <div className="flex-1 w-full bg-card p-6 rounded-2xl border border-border shadow-2xl">
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between text-xs text-muted-foreground uppercase font-bold tracking-wider">
                    <span>Raw Footage</span>
                    <span className="text-destructive">10:00 min</span>
                  </div>
                  <div className="h-16 bg-muted rounded border border-border relative overflow-hidden flex items-center px-2 gap-1">
                    <div className="h-8 w-[10%] bg-muted-foreground rounded-sm" />
                    <div className="h-[1px] w-[15%] bg-destructive/30 border-t border-dotted border-destructive" />
                    <div className="h-10 w-[20%] bg-muted-foreground rounded-sm" />
                    <div className="h-[1px] w-[10%] bg-destructive/30 border-t border-dotted border-destructive" />
                    <div className="h-6 w-[15%] bg-muted-foreground rounded-sm" />
                    <div className="h-[1px] w-[20%] bg-destructive/30 border-t border-dotted border-destructive" />
                    <div className="h-8 w-[10%] bg-muted-foreground rounded-sm" />
                  </div>
                </div>
                <div className="flex justify-center -my-3 z-10">
                  <div className="bg-primary rounded-full p-2 text-primary-foreground shadow-lg">
                    <ArrowDown className="h-5 w-5" />
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <div className="flex justify-between text-xs text-muted-foreground uppercase font-bold tracking-wider">
                    <span>AI Processed</span>
                    <span className="text-primary">4:20 min</span>
                  </div>
                  <div className="h-16 bg-muted rounded border border-primary/30 shadow-[0_0_15px_rgba(57,224,121,0.15)] relative overflow-hidden flex items-center px-2 gap-[1px]">
                    <div className="h-8 w-[24%] bg-primary rounded-l-sm" />
                    <div className="h-10 w-[38%] bg-primary" />
                    <div className="h-6 w-[28%] bg-primary" />
                    <div className="h-8 w-[10%] bg-primary rounded-r-sm" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      {/* <section
        className="py-20 px-6 lg:px-40 bg-card border-t border-border"
        id="pricing"
      >
        <div className="max-w-[960px] mx-auto flex flex-col gap-12">
          <div className="text-center">
            <h2 className="text-3xl md:text-4xl font-black leading-tight mb-4 text-foreground">
              Simple, Transparent Pricing
            </h2>
            <p className="text-muted-foreground">Start for free, upgrade for power.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            // Free 
            <div className="flex flex-col gap-6 rounded-xl border border-border bg-background p-8">
              <div>
                <h3 className="text-foreground text-lg font-bold">Free</h3>
                <div className="flex items-baseline gap-1 mt-2 text-foreground">
                  <span className="text-4xl font-black tracking-tighter">$0</span>
                  <span className="text-sm font-medium opacity-60">/mo</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Perfect for hobbyists.</p>
              </div>
              <Link href="/register">
                <Button variant="outline" className="w-full">
                  Download Now
                </Button>
              </Link>
              <div className="flex flex-col gap-3">
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  Basic silence removal
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  720p Export
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-muted-foreground" />
                  Watermarked
                </div>
              </div>
            </div>

            // Pro 
            <div className="flex flex-col gap-6 rounded-xl border-2 border-primary bg-background p-8 relative shadow-2xl shadow-primary/10">
              <div className="absolute top-0 right-0 bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">
                POPULAR
              </div>
              <div>
                <h3 className="text-foreground text-lg font-bold">Pro Creator</h3>
                <div className="flex items-baseline gap-1 mt-2 text-foreground">
                  <span className="text-4xl font-black tracking-tighter">$18</span>
                  <span className="text-sm font-medium opacity-60">/mo</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">For serious YouTubers.</p>
              </div>
              <Link href="/register">
                <Button className="w-full shadow-lg shadow-primary/25">Start Free Trial</Button>
              </Link>
              <div className="flex flex-col gap-3">
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  <strong>Everything in Free</strong>
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  No Watermarks
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  4K Export
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  Advanced Word Filtering
                </div>
              </div>
            </div>

            // Studio 
            <div className="flex flex-col gap-6 rounded-xl border border-border bg-background p-8">
              <div>
                <h3 className="text-foreground text-lg font-bold">Studio</h3>
                <div className="flex items-baseline gap-1 mt-2 text-foreground">
                  <span className="text-4xl font-black tracking-tighter">$45</span>
                  <span className="text-sm font-medium opacity-60">/mo</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">Agencies & Teams.</p>
              </div>
              <Button variant="outline" className="w-full">
                Contact Sales
              </Button>
              <div className="flex flex-col gap-3">
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  Team Collaboration
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  API Access
                </div>
                <div className="text-sm flex gap-3 text-muted-foreground">
                  <Check className="h-5 w-5 text-primary" />
                  Dedicated Support
                </div>
              </div>
            </div>
          </div>
        </div>
      </section> */}

      {/* Footer */}
      <footer className="bg-background border-t border-border pt-16 pb-8 px-6 lg:px-40">
        <div className="max-w-[960px] mx-auto flex flex-col gap-12">
          <div className="flex flex-col md:flex-row justify-between gap-8">
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-2 text-foreground">
                <Scissors className="h-6 w-6 text-primary" />
                <h2 className="text-lg font-bold">ClipFlow</h2>
              </div>
              <p className="text-sm text-muted-foreground max-w-xs">
                The privacy-first video editor that saves you hours of work. Built for creators who
                value their time and data.
              </p>
            </div>
            <div className="flex gap-12 flex-wrap">
              <div className="flex flex-col gap-3">
                <h4 className="text-sm font-bold text-foreground uppercase tracking-wider">
                  Product
                </h4>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#features"
                >
                  Features
                </a>
                {/* <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#pricing"
                >
                  Pricing
                </a> */}
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Download
                </a>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Changelog
                </a>
              </div>
              <div className="flex flex-col gap-3">
                <h4 className="text-sm font-bold text-foreground uppercase tracking-wider">
                  Resources
                </h4>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Documentation
                </a>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Community
                </a>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Blog
                </a>
              </div>
              <div className="flex flex-col gap-3">
                <h4 className="text-sm font-bold text-foreground uppercase tracking-wider">
                  Legal
                </h4>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Privacy Policy
                </a>
                <a
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  href="#"
                >
                  Terms of Service
                </a>
              </div>
            </div>
          </div>
          <div className="border-t border-border pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground">
              2024 ClipFlow Inc. All rights reserved.
            </p>
            <div className="flex gap-4">
              <a className="text-muted-foreground hover:text-primary transition-colors" href="#">
                <Twitter className="h-5 w-5" />
              </a>
              <a className="text-muted-foreground hover:text-primary transition-colors" href="#">
                <Github className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
