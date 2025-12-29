"use client";

import { useState, useCallback, useMemo, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  Upload,
  Shield,
  AudioWaveform,
  MessageSquareWarning,
  Subtitles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { projectsApi, analysisApi, configApi } from "@/lib/api";
import { cn, formatFileSize } from "@/lib/utils";

type Step = 1 | 2 | 3;

export default function NewProjectPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>(1);
  const hasProcessedPreSelectedFileRef = useRef(false);
  const [file, setFile] = useState<File | null>(null);
  const [projectName, setProjectName] = useState("");
  const [aspectRatio, setAspectRatio] = useState<"16:9" | "9:16" | "1:1">("16:9");

  // Fetch features config
  const { data: featuresConfig } = useQuery({
    queryKey: ["features"],
    queryFn: () => configApi.getFeatures(),
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
  const [uploadProgress, setUploadProgress] = useState(0);
  const [aiSettings, setAiSettings] = useState({
    silenceRemoval: true,
    profanityFilter: false,
    autoCaptions: false,
  });
  const [thumbnail, setThumbnail] = useState<Blob | null>(null);

  useEffect(() => {
    // Check for pre-selected file from dashboard (run only once on mount)
    if (hasProcessedPreSelectedFileRef.current) return; // Prevent multiple executions

    const selectedFile = globalThis.__selectedFile;
    if (selectedFile) { // Only check for selectedFile, no need to check !file since this runs on mount
      try {
        hasProcessedPreSelectedFileRef.current = true; // Set flag immediately
        const fileData = selectedFile;

        // Clear global variable immediately to prevent re-processing
        globalThis.__selectedFile = null;

        // Set file state and move to step 2
        setFile(fileData);
        setProjectName(fileData.name.replace(/\.[^/.]+$/, ""));
        setStep(2);

        // Generate thumbnail in background
        generateThumbnail(fileData).then((thumbBlob) => {
          setThumbnail(thumbBlob);
        }).catch((error) => {
          console.error("Failed to generate thumbnail:", error);
        });

      } catch (error) {
        console.error('Failed to process selected file:', error);
      }
    }
  }, []); // Empty dependency array - run only once on mount

  const createProjectMutation = useMutation({
    mutationFn: async () => {
      if (!file) throw new Error("No file selected");

      const project = await projectsApi.create({
        name: projectName || file.name.replace(/\.[^/.]+$/, ""),
        processing_options: {
          silence_removal: aiSettings.silenceRemoval,
          filler_word_filter: aiSettings.profanityFilter,
        },
      });

      await projectsApi.uploadMedia(project.id, file, (progress) => {
        setUploadProgress(progress);
      });

      // Upload thumbnail if available
      if (thumbnail) {
        await projectsApi.uploadThumbnail(project.id, thumbnail);
      }

      // Start analysis with settings
      const mediaResponse = await projectsApi.get(project.id);
      if (mediaResponse.media_files.length > 0) {
        await analysisApi.start(mediaResponse.media_files[0].id, {
          processing_mode: aiSettings.profanityFilter ? "whisper" : "auto",
          detect_filler_words: aiSettings.profanityFilter,
        });
      }

      return project;
    },
    onSuccess: (project) => {
      router.push(`/projects/${project.id}`);
    },
  });

  const generateThumbnail = useCallback((videoFile: File): Promise<Blob> => {
    return new Promise((resolve, reject) => {
      const video = document.createElement("video");
      video.preload = "metadata";
      video.muted = true;
      video.playsInline = true;

      video.onloadeddata = () => {
        // Seek to 1 second or 10% of the video, whichever is smaller
        video.currentTime = Math.min(1, video.duration * 0.1);
      };

      video.onseeked = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          reject(new Error("Failed to get canvas context"));
          return;
        }

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error("Failed to generate thumbnail"));
            }
            URL.revokeObjectURL(video.src);
          },
          "image/jpeg",
          0.8
        );
      };

      video.onerror = () => {
        reject(new Error("Failed to load video"));
        URL.revokeObjectURL(video.src);
      };

      video.src = URL.createObjectURL(videoFile);
    });
  }, []);

  const handleFileSelect = useCallback(async (selectedFile: File) => {
    setFile(selectedFile);
    setProjectName(selectedFile.name.replace(/\.[^/.]+$/, ""));
    setStep(2);

    // Generate thumbnail in background
    try {
      const thumbBlob = await generateThumbnail(selectedFile);
      setThumbnail(thumbBlob);
    } catch (error) {
      console.error("Failed to generate thumbnail:", error);
    }
  }, [generateThumbnail]);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const droppedFile = e.dataTransfer.files?.[0];
      if (droppedFile && droppedFile.type.startsWith("video/")) {
        handleFileSelect(droppedFile);
      }
    },
    [handleFileSelect]
  );

  const thumbnailPreviewUrl = useMemo(() => {
    if (thumbnail) {
      return URL.createObjectURL(thumbnail);
    }
    return null;
  }, [thumbnail]);

  useEffect(() => {
    // Check for pre-selected file from dashboard (run only once on mount)
    const selectedFileData = sessionStorage.getItem('selectedFile');
    if (selectedFileData && !file) { // Only process if we haven't set a file yet
      try {
        const fileData = JSON.parse(selectedFileData);

        // Reconstruct File object from base64 data
        const binaryString = atob(fileData.data);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }

        const reconstructedFile = new File([bytes], fileData.name, {
          type: fileData.type,
          lastModified: fileData.lastModified,
        });

        // Clear sessionStorage and set the file
        sessionStorage.removeItem('selectedFile');
        setFile(reconstructedFile);
        setProjectName(reconstructedFile.name.replace(/\.[^/.]+$/, ""));
        setStep(2);

        // Generate thumbnail in background
        generateThumbnail(reconstructedFile).then((thumbBlob) => {
          setThumbnail(thumbBlob);
        }).catch((error) => {
          console.error("Failed to generate thumbnail:", error);
        });
      } catch (error) {
        console.error('Failed to reconstruct file from sessionStorage:', error);
        sessionStorage.removeItem('selectedFile');
      }
    }
  }, []); // Empty dependency array - run only once on mount

  const handleSubmit = () => {
    setStep(3);
    createProjectMutation.mutate();
  };

  return (
    <div className="flex-grow flex flex-col items-center justify-start py-8 px-4 md:px-8">
      <div className="w-full max-w-4xl flex flex-col gap-8">
        {/* Progress Stepper */}
        <div className="w-full">
          <div className="flex items-center justify-between relative mb-8">
            <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-muted rounded-full -z-10" />
            {step >= 2 && (
              <div className="absolute left-[10%] top-1/2 transform -translate-y-1/2 w-[40%] h-1 bg-primary rounded-full -z-10" />
            )}
            {step >= 3 && (
              <div className="absolute left-[10%] top-1/2 transform -translate-y-1/2 w-[80%] h-1 bg-primary rounded-full -z-10" />
            )}

            {/* Step 1 */}
            <div className="flex flex-col items-center gap-2">
              <div
                className={cn(
                  "size-10 rounded-full flex items-center justify-center font-bold border-4 border-background shadow-lg",
                  step >= 1 ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                )}
              >
                {step > 1 ? <Check className="h-5 w-5" /> : "1"}
              </div>
              <span
                className={cn(
                  "text-xs font-semibold uppercase tracking-wider",
                  step >= 1 ? "text-primary" : "text-muted-foreground"
                )}
              >
                Upload
              </span>
            </div>

            {/* Step 2 */}
            <div className="flex flex-col items-center gap-2">
              <div
                className={cn(
                  "size-10 rounded-full flex items-center justify-center font-bold border-4 border-background",
                  step >= 2 ? "bg-primary text-primary-foreground shadow-[0_0_15px_rgba(57,224,121,0.4)]" : "bg-muted text-muted-foreground"
                )}
              >
                {step > 2 ? <Check className="h-5 w-5" /> : "2"}
              </div>
              <span
                className={cn(
                  "text-xs font-semibold uppercase tracking-wider",
                  step >= 2 ? "text-foreground" : "text-muted-foreground"
                )}
              >
                Details & AI
              </span>
            </div>

            {/* Step 3 */}
            <div className="flex flex-col items-center gap-2">
              <div
                className={cn(
                  "size-10 rounded-full flex items-center justify-center font-bold border-4 border-background",
                  step >= 3 ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                )}
              >
                3
              </div>
              <span
                className={cn(
                  "text-xs font-semibold uppercase tracking-wider",
                  step >= 3 ? "text-foreground" : "text-muted-foreground"
                )}
              >
                Review
              </span>
            </div>
          </div>
        </div>

        {/* Step 1: Upload */}
        {step === 1 && (
          <div className="flex flex-col gap-6">
            <div className="text-center md:text-left">
              <h2 className="text-3xl font-black text-foreground mb-2">Upload Your Video</h2>
              <p className="text-muted-foreground">
                Drag and drop your video file or click to browse.
              </p>
            </div>

            <div
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className="relative flex min-h-[400px] cursor-pointer flex-col items-center justify-center gap-6 rounded-2xl border-2 border-dashed border-border bg-muted/30 p-8 text-center transition-all hover:border-primary hover:bg-primary/5"
            >
              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-muted text-muted-foreground">
                <Upload className="h-10 w-10" />
              </div>
              <div className="space-y-2">
                <h4 className="text-xl font-bold text-foreground">
                  Drop your video here
                </h4>
                <p className="text-sm text-muted-foreground">
                  Supports MP4, MOV, WebM up to 500MB
                </p>
              </div>
              <Button variant="outline" onClick={() => document.getElementById("file-input")?.click()}>
                Browse Files
              </Button>
              <input
                id="file-input"
                type="file"
                accept="video/*"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) handleFileSelect(f);
                }}
                className="hidden"
              />
            </div>
          </div>
        )}

        {/* Step 2: Details & AI */}
        {step === 2 && file && (
          <div className="flex flex-col gap-6">
            <div className="text-center md:text-left">
              <h2 className="text-3xl font-black text-foreground mb-2">Configure Project</h2>
              <p className="text-muted-foreground">
                Customize your video settings and select AI enhancements.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Column: Source Video */}
              <div className="lg:col-span-4 flex flex-col gap-4">
                <div className="bg-card border border-border rounded-xl p-4 flex flex-col gap-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-semibold text-foreground">Source Video</h3>
                    <button
                      onClick={() => setStep(1)}
                      className="text-xs text-primary hover:underline"
                    >
                      Change
                    </button>
                  </div>
                  <div className="aspect-video w-full bg-muted rounded-lg overflow-hidden relative flex items-center justify-center">
                    {thumbnailPreviewUrl ? (
                      <img
                        src={thumbnailPreviewUrl}
                        alt="Video thumbnail"
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="animate-pulse flex items-center justify-center">
                        <span className="text-muted-foreground text-sm">Generating thumbnail...</span>
                      </div>
                    )}
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="bg-muted p-2 rounded text-muted-foreground">
                      <span className="material-symbols-outlined text-xl">movie</span>
                    </div>
                    <div className="flex flex-col overflow-hidden">
                      <span className="text-foreground text-sm font-medium truncate">
                        {file.name}
                      </span>
                      <span className="text-muted-foreground text-xs">
                        {formatFileSize(file.size)}
                      </span>
                    </div>
                  </div>
                </div>

                {/* <div className="bg-primary/5 border border-primary/20 rounded-xl p-4 flex items-start gap-3">
                  <Shield className="h-5 w-5 text-primary mt-0.5" />
                  <div className="flex flex-col gap-1">
                    <p className="text-primary text-sm font-bold">Privacy Guaranteed</p>
                    <p className="text-muted-foreground text-xs leading-relaxed">
                      Your video remains on your device. Our AI models run locally in your browser.
                    </p>
                  </div>
                </div> */}
              </div>

              {/* Right Column: Form */}
              <div className="lg:col-span-8 flex flex-col gap-6">
                {/* Basic Info */}
                <div className="bg-card border border-border rounded-xl p-6">
                  <div className="flex flex-col gap-5">
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="project-name">Project Name</Label>
                      <Input
                        id="project-name"
                        value={projectName}
                        onChange={(e) => setProjectName(e.target.value)}
                        placeholder="e.g. Weekly Vlog - Episode 4"
                      />
                    </div>

                    {/* <div className="flex flex-col gap-2">
                      <Label>Canvas Format</Label>
                      <div className="grid grid-cols-3 gap-3">
                        {(["16:9", "9:16", "1:1"] as const).map((ratio) => (
                          <label key={ratio} className="cursor-pointer">
                            <input
                              type="radio"
                              name="aspect"
                              checked={aspectRatio === ratio}
                              onChange={() => setAspectRatio(ratio)}
                              className="peer sr-only"
                            />
                            <div className="flex flex-col items-center gap-2 p-3 rounded-lg border border-border bg-background peer-checked:border-primary peer-checked:bg-primary/10 transition-all hover:border-muted-foreground">
                              <div
                                className={cn(
                                  "border-2 border-current rounded-sm",
                                  ratio === "16:9" && "w-8 h-5",
                                  ratio === "9:16" && "w-5 h-8",
                                  ratio === "1:1" && "w-6 h-6",
                                  aspectRatio === ratio ? "text-primary" : "text-muted-foreground"
                                )}
                              />
                              <span className="text-xs font-medium text-muted-foreground peer-checked:text-foreground">
                                {ratio === "16:9" && "Landscape"}
                                {ratio === "9:16" && "Portrait"}
                                {ratio === "1:1" && "Square"}
                              </span>
                            </div>
                          </label>
                        ))}
                      </div>
                    </div> */}
                  </div>
                </div>

                {/* AI Settings */}
                <div className="bg-card border border-border rounded-xl p-6">
                  <div className="flex items-center gap-2 mb-6">
                    <span className="material-symbols-outlined text-primary">auto_fix_high</span>
                    <h3 className="text-foreground text-lg font-bold">AI Magic Tools</h3>
                  </div>

                  <div className="space-y-6">
                    {/* Silence Removal */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-start gap-4">
                        <div className="bg-muted p-2.5 rounded-lg text-primary">
                          <AudioWaveform className="h-5 w-5" />
                        </div>
                        <div>
                          <p className="text-foreground font-medium mb-1">Silence Removal</p>
                          <p className="text-muted-foreground text-sm">
                            Automatically cuts pauses longer than 0.5s.
                          </p>
                        </div>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={aiSettings.silenceRemoval}
                          disabled={true}
                          // onChange={(e) =>
                          //   setAiSettings({ ...aiSettings, silenceRemoval: e.target.checked })
                          // }
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all" />
                      </label>
                    </div>

                    {featuresConfig?.filler_detection_available && (
                      <>
                        <hr className="border-border" />

                        {/* Filler Word Filter */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-start gap-4">
                            <div className="bg-muted p-2.5 rounded-lg text-primary">
                              <MessageSquareWarning className="h-5 w-5" />
                            </div>
                            <div>
                              <p className="text-foreground font-medium mb-1">Filler Word Filter</p>
                              <p className="text-muted-foreground text-sm">
                                Removes filler words like "um", "uh", and "like".
                              </p>
                            </div>
                          </div>
                          <label className="relative inline-flex items-center cursor-pointer">
                            <input
                              type="checkbox"
                              checked={aiSettings.profanityFilter}
                              onChange={(e) =>
                                setAiSettings({ ...aiSettings, profanityFilter: e.target.checked })
                              }
                              className="sr-only peer"
                            />
                            <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all" />
                          </label>
                        </div>
                      </>
                    )}

                    {/* <hr className="border-border" />

                    Auto Captions
                    <div className="flex items-center justify-between">
                      <div className="flex items-start gap-4">
                        <div className="bg-muted p-2.5 rounded-lg text-primary">
                          <Subtitles className="h-5 w-5" />
                        </div>
                        <div>
                          <p className="text-foreground font-medium mb-1">Auto Captions</p>
                          <p className="text-muted-foreground text-sm">
                            Generate subtitles from audio track.
                          </p>
                        </div>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={aiSettings.autoCaptions}
                          onChange={(e) =>
                            setAiSettings({ ...aiSettings, autoCaptions: e.target.checked })
                          }
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:bg-primary peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all" />
                      </label>
                    </div> */}
                  </div>
                </div>
              </div>
            </div>

            {/* Footer Navigation */}
            <div className="flex items-center justify-between pt-6 border-t border-border mt-2">
              <Button variant="ghost" onClick={() => setStep(1)}>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
              <Button 
                onClick={handleSubmit}
                disabled={!aiSettings.silenceRemoval && !aiSettings.profanityFilter}
              >
                Next Step
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>
        )}

        {/* Step 3: Processing */}
        {step === 3 && (
          <div className="flex flex-col items-center justify-center gap-8 py-16">
            <div className="flex flex-col items-center gap-4">
              <div className="h-16 w-16 animate-spin rounded-full border-4 border-primary border-t-transparent" />
              <h2 className="text-2xl font-bold text-foreground">Processing Your Video</h2>
              <p className="text-muted-foreground text-center max-w-md">
                We&apos;re analyzing your video and applying AI enhancements. This may take a few
                moments.
              </p>
            </div>

            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="w-full max-w-md">
                <div className="flex justify-between text-sm text-muted-foreground mb-2">
                  <span>Uploading...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary transition-all"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              </div>
            )}

            {createProjectMutation.isError && (
              <div className="flex flex-col items-center gap-4">
                <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-sm">
                  Failed to create project. Please try again.
                </div>
                <Button
                  variant="outline"
                  onClick={() => {
                    createProjectMutation.reset();
                    setStep(2);
                  }}
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Go Back
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
