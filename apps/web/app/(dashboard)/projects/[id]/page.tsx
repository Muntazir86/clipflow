"use client";

import { useEffect, useRef, useState, useCallback, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  ArrowLeft,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  ZoomIn,
  ZoomOut,
  Scissors,
  Filter,
  Download,
  AudioWaveform,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { projectsApi, analysisApi, mediaApi } from "@/lib/api";
import { cn, formatDurationMs } from "@/lib/utils";
import { useEditorStore } from "@/stores/editor-store";

export default function ProjectEditorPage() {
  const params = useParams();
  const router = useRouter();
  const queryClient = useQueryClient();
  const projectId = params.id as string;

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isVideoProcessed, setIsVideoProcessed] = useState(false);
  const [processedMediaId, setProcessedMediaId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"original" | "processed">("original");
  const videoRef = useRef<HTMLVideoElement>(null);
  const processedVideoRef = useRef<HTMLVideoElement>(null);

  const { setProject, setAnalysisResult, segments, reset } = useEditorStore();

  // Reset editor store when project changes to prevent data overlapping
  useEffect(() => {
    reset();
  }, [projectId, reset]);

  // Fetch project data
  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.get(projectId),
  });

  // Get the latest analysis ID
  const analysisId = project?.media_files?.[0]?.analysis_results?.[0]?.id;

  // Fetch analysis data
  const { data: analysis } = useQuery({
    queryKey: ["analysis", analysisId],
    queryFn: () => (analysisId ? analysisApi.get(analysisId) : null),
    enabled: !!analysisId,
    refetchInterval: (query) => {
      const data = query.state.data;
      return data?.status === "processing" ? 4000 : false;
    },
  });

  // Fetch waveform data
  const mediaFileId = project?.media_files?.[0]?.id;
  const { data: waveformData } = useQuery({
    queryKey: ["waveform", mediaFileId],
    queryFn: () => (mediaFileId ? mediaApi.getWaveform(mediaFileId) : null),
    enabled: !!mediaFileId,
  });

  // Memoize max peak calculation to avoid recalculating on each render
  const maxPeak = useMemo(() => {
    if (!waveformData?.peaks || waveformData.peaks.length === 0) return 0;
    return Math.max(...waveformData.peaks.map(p => Math.abs(p)));
  }, [waveformData?.peaks]);

  // Update store when data changes
  useEffect(() => {
    if (project) {
      setProject(project);
    }
  }, [project, setProject]);

  useEffect(() => {
    if (analysis) {
      setAnalysisResult(analysis);
    }
  }, [analysis, setAnalysisResult]);

  const mediaFile = project?.media_files?.[0];
  const duration = mediaFile?.duration_seconds || 0;
  const isProcessing = analysis?.status === "processing" || analysis?.status === "pending";

  // Get processing options from project
  const processingOptions = project?.processing_options;
  const shouldProcessSilence = processingOptions?.silence_removal ?? true;
  const shouldProcessFillerWords = processingOptions?.filler_word_filter ?? false;

  const silenceCount = segments.filter((s) => s.type === "silence").length;
  const fillerCount = segments.filter((s) => s.type === "filler").length;

  // Count segments that will be processed based on options
  const segmentsToProcess = segments.filter((s) => 
    (s.type === "silence" && shouldProcessSilence) || 
    (s.type === "filler" && shouldProcessFillerWords)
  ).length;

  // Get video stream URL
  const videoStreamUrl = mediaFile ? mediaApi.getStreamUrl(mediaFile.id) : null;

  // Get processed video stream URL (find the latest processed file)
  const processedMediaFile = project?.media_files?.find(
    (f) => f.id === processedMediaId || f.original_filename.includes("_processed_")
  );
  const processedVideoStreamUrl = processedMediaFile 
    ? mediaApi.getStreamUrl(processedMediaFile.id) 
    : null;

  // Video playback controls
  const togglePlayPause = useCallback(() => {
    if (!videoRef.current) return;
    
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setIsPlaying(!isPlaying);
  }, [isPlaying]);

  const handleTimeUpdate = useCallback(() => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  }, []);

  const handleVideoEnded = useCallback(() => {
    setIsPlaying(false);
  }, []);

  const skipBackward = useCallback(() => {
    if (videoRef.current) {
      videoRef.current.currentTime = Math.max(0, videoRef.current.currentTime - 5);
    }
  }, []);

  const skipForward = useCallback(() => {
    if (videoRef.current) {
      videoRef.current.currentTime = Math.min(duration, videoRef.current.currentTime + 5);
    }
  }, [duration]);

  // Timeline ref for seek calculations
  const timelineRef = useRef<HTMLDivElement>(null);

  // Seek to position based on click/drag on timeline
  const seekToPosition = useCallback((clientX: number) => {
    if (!timelineRef.current || !videoRef.current || duration === 0) return;
    
    const rect = timelineRef.current.getBoundingClientRect();
    const scrollLeft = timelineRef.current.scrollLeft;
    const totalWidth = timelineRef.current.scrollWidth;
    
    // Calculate position relative to the scrollable content
    const clickX = clientX - rect.left + scrollLeft;
    const percentage = Math.max(0, Math.min(1, clickX / totalWidth));
    const newTime = percentage * duration;
    
    videoRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  }, [duration]);

  // Handle timeline click
  const handleTimelineClick = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    seekToPosition(e.clientX);
  }, [seekToPosition]);

  // Handle playhead drag
  const [isDragging, setIsDragging] = useState(false);

  const handlePlayheadMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      seekToPosition(e.clientX);
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, seekToPosition]);

  // process Video mutation
  const processVideoMutation = useMutation({
    mutationFn: async () => {
      if (!mediaFileId) throw new Error("No media file");
      if (!project?.processing_options) throw new Error("No processing options available");
      
      return mediaApi.processVideo(mediaFileId, {
        silence_removal: project.processing_options.silence_removal,
        filler_word_filter: project.processing_options.filler_word_filter,
      });
    },
    onMutate: async () => {
      setIsVideoProcessed(true);
      // Update project status to processing
      if (projectId) {
        await projectsApi.update(projectId, { status: "processing" });
        queryClient.invalidateQueries({ queryKey: ["project", projectId] });
      }
    },
    onSuccess: async (newMediaFile) => {
      setProcessedMediaId(newMediaFile.id);
      // Update project status to completed
      if (projectId) {
        await projectsApi.update(projectId, { status: "completed" });
      }
      // Invalidate project query to refresh media files list
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
      setIsVideoProcessed(false);
    },
    onError: async (error) => {
      console.error("Failed to process video:", error);
      // Update project status to failed
      if (projectId) {
        await projectsApi.update(projectId, { status: "failed" });
        queryClient.invalidateQueries({ queryKey: ["project", projectId] });
      }
      setIsVideoProcessed(false);
    },
  });

  const handleProcessVideo = useCallback(() => {
    if (silenceCount === 0 && fillerCount === 0) return;
    processVideoMutation.mutate();
  }, [silenceCount, fillerCount, processVideoMutation]);

  // Handle download of processed video (must be before early returns)
  const handleDownloadProcessed = useCallback(() => {
    if (!processedVideoStreamUrl || !processedMediaFile) return;
    const link = document.createElement('a');
    link.href = processedVideoStreamUrl;
    link.download = processedMediaFile.original_filename || 'processed_video.mp4';
    link.click();
  }, [processedVideoStreamUrl, processedMediaFile]);

  if (projectLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          <p className="text-sm text-muted-foreground">Loading project...</p>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-foreground">Project not found</h2>
          <Button variant="outline" className="mt-4" onClick={() => router.push("/dashboard")}>
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  // Check if video has been processed
  const hasProcessedVideo = !!processedVideoStreamUrl;

  return (
    <div className="flex flex-1 flex-col min-w-0 bg-background relative">
      {/* Header */}
      <header className="bg-card border-b border-border shrink-0 z-10">
        {/* Mobile Header */}
        <div className="flex md:hidden h-14 items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" onClick={() => router.push("/dashboard")}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <h1 className="text-base font-semibold text-foreground truncate max-w-[120px]">{project.name}</h1>
          </div>

          {/* Mobile Tab Selector */}
          <div className="flex items-center gap-2">
            <select
              value={activeTab}
              onChange={(e) => setActiveTab(e.target.value as "original" | "processed")}
              className="px-2 py-1 text-sm bg-muted border border-border rounded-md text-foreground"
            >
              <option value="original">Original</option>
              <option value="processed">Processed</option>
            </select>

            {activeTab === "original" ? (
              <Button
                size="sm"
                disabled={isProcessing || isVideoProcessed || segmentsToProcess === 0 || hasProcessedVideo}
                onClick={handleProcessVideo}
              >
                <Scissors className="h-4 w-4" />
              </Button>
            ) : (
              <Button
                size="sm"
                disabled={!hasProcessedVideo}
                onClick={handleDownloadProcessed}
              >
                <Download className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>

        {/* Desktop Header */}
        <div className="hidden md:flex h-16 items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => router.push("/dashboard")}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <h1 className="text-lg font-semibold text-foreground">{project.name}</h1>
          </div>

          {/* Tabs */}
          <div className="flex items-center gap-1 bg-muted p-1 rounded-lg">
            <button
              onClick={() => setActiveTab("original")}
              className={cn(
                "px-4 py-1.5 text-sm font-medium rounded-md transition-all",
                activeTab === "original"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              Original
            </button>
            <button
              onClick={() => setActiveTab("processed")}
              className={cn(
                "px-4 py-1.5 text-sm font-medium rounded-md transition-all",
                activeTab === "processed"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground",
                hasProcessedVideo && activeTab !== "processed" && "text-primary"
              )}
            >
              Processed
              {hasProcessedVideo && (
                <span className="ml-1.5 w-2 h-2 rounded-full bg-primary inline-block" />
              )}
            </button>
          </div>

          <div className="flex items-center gap-3">
            {activeTab === "original" ? (
              <Button
                size="sm"
                disabled={isProcessing || isVideoProcessed || segmentsToProcess === 0 || hasProcessedVideo}
                onClick={handleProcessVideo}
              >
                {isVideoProcessed ? (
                  <>
                    <div className="h-4 w-4 mr-2 animate-spin rounded-full border-2 border-current border-t-transparent" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Scissors className="h-4 w-4 mr-2" />
                    Process Video
                  </>
                )}
              </Button>
            ) : (
              <Button
                size="sm"
                disabled={!hasProcessedVideo}
                onClick={handleDownloadProcessed}
              >
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden flex flex-col gap-4 lg:gap-6 p-3 sm:p-4 lg:p-6 min-h-0">
        {activeTab === "original" ? (
          <>
            {/* Original Video Preview */}
            <div className="flex justify-center relative bg-black/40 rounded-2xl border border-border overflow-hidden max-h-[45vh] lg:max-h-[50vh] xl:max-h-[60vh] group">
              <div className="relative h-full aspect-video bg-black shadow-2xl flex items-center justify-center max-h-full">
                {videoStreamUrl ? (
                  <video
                    ref={videoRef}
                    src={videoStreamUrl}
                    className="w-full h-full object-contain"
                    onTimeUpdate={handleTimeUpdate}
                    onEnded={handleVideoEnded}
                    onPlay={() => setIsPlaying(true)}
                    onPause={() => setIsPlaying(false)}
                  />
                ) : (
                  <p className="text-muted-foreground">No video uploaded</p>
                )}

                {/* Overlay controls on hover */}
                {videoStreamUrl && (
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-between p-6">
                    <div className="flex justify-between items-start">
                      <div className="bg-black/60 backdrop-blur px-3 py-1 rounded text-xs font-mono text-primary border border-primary/20">
                        {mediaFile?.original_filename}
                      </div>
                    </div>
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <button
                        onClick={togglePlayPause}
                        className="w-20 h-20 rounded-full bg-primary/20 backdrop-blur-sm border border-primary/30 flex items-center justify-center text-white pointer-events-auto hover:scale-110 hover:bg-primary/40 transition-all shadow-[0_0_30px_rgba(57,224,121,0.3)]"
                      >
                        {isPlaying ? (
                          <Pause className="h-10 w-10" />
                        ) : (
                          <Play className="h-10 w-10 ml-1" />
                        )}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Timeline Panel */}
            <div className="flex-1 min-h-0 bg-card border border-border rounded-2xl p-5 shadow-2xl relative z-20 overflow-hidden">
              {/* Timeline Header */}
              <div className="flex justify-between items-center mb-4 px-1">
                <div className="flex items-center gap-6">
                  <div className="text-sm font-medium text-foreground flex items-center gap-2">
                    <AudioWaveform className="h-5 w-5 text-primary" />
                    Audio Timeline
                  </div>
                  <div className="h-4 w-px bg-border" />
                  <div className="flex gap-4 text-xs">
                    {shouldProcessSilence && (
                      <div className="flex items-center gap-2 cursor-help" title="Low volume segments - will be removed">
                        <div className="w-2 h-2 rounded-sm bg-red-500/50 ring-1 ring-red-500" />
                        <span className="text-muted-foreground">Silence</span>
                      </div>
                    )}
                    {shouldProcessFillerWords && (
                      <div className="flex items-center gap-2 cursor-help" title="Detected filler words - will be removed">
                        <div className="w-2 h-2 rounded-sm bg-blue-500/50 ring-1 ring-blue-500" />
                        <span className="text-muted-foreground">Filler Words</span>
                      </div>
                    )}
                    {!shouldProcessSilence && !shouldProcessFillerWords && (
                      <span className="text-muted-foreground">No processing options selected</span>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 text-primary font-mono text-sm bg-muted px-3 py-1 rounded border border-border">
                  <span>{formatDurationMs(currentTime * 1000)}</span>
                  <span className="text-muted-foreground">/</span>
                  <span className="text-muted-foreground">{formatDurationMs(duration * 1000)}</span>
                </div>
              </div>

              {/* Waveform Timeline */}
              <div className="flex">
                <div className="flex-1 flex flex-col">
                  <div 
                    ref={timelineRef}
                    onClick={handleTimelineClick}
                    className="relative min-h-[70px] h-12 lg:h-14 bg-muted/30 rounded-lg border border-border overflow-x-auto overflow-y-hidden group select-none cursor-pointer">
                    {isProcessing ? (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="flex flex-col items-center gap-2">
                          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                          <span className="text-xs text-muted-foreground">Analyzing audio...</span>
                        </div>
                      </div>
                    ) : (
                      <div 
                        className="relative h-full transition-all duration-200"
                        style={{ width: `${100 * zoomLevel}%`, minWidth: '100%' }}
                      >
                        {/* Playhead */}
                        <div
                          onMouseDown={handlePlayheadMouseDown}
                          className={cn(
                            "absolute top-0 bottom-0 w-0.5 bg-primary z-30 shadow-[0_0_10px_rgba(57,224,121,0.5)] cursor-ew-resize",
                            isDragging && "w-1"
                          )}
                          style={{ left: `${(currentTime / duration) * 100}%` }}
                        >
                          <div className="absolute -top-1 -left-[5px] w-3 h-3 bg-primary rotate-45 rounded-sm cursor-ew-resize" />
                        </div>

                        {/* Actual Waveform visualization */}
                        <div className="absolute inset-0 flex items-center px-1 z-0">
                          {waveformData?.peaks && waveformData.peaks.length > 0 ? (
                            <div className="flex items-center justify-between h-full w-full">
                              {waveformData.peaks.map((peak, idx) => {
                                const normalizedHeight = maxPeak > 0 
                                  ? (Math.abs(peak) / maxPeak) * 100 
                                  : 0;
                                return (
                                  <div
                                    key={idx}
                                    className="bg-primary/70 rounded-sm"
                                    style={{ 
                                      height: `${Math.max(normalizedHeight, 3)}%`,
                                      width: `${Math.max(100 / waveformData.peaks.length - 0.5, 1)}%`
                                    }}
                                  />
                                );
                              })}
                            </div>
                          ) : (
                            <div className="flex items-center justify-between h-full w-full opacity-50">
                              {[...Array(80)].map((_, i) => (
                                <div
                                  key={i}
                                  className="bg-primary/40 rounded-sm"
                                  style={{ 
                                    height: `${20 + Math.sin(i * 0.3) * 30}%`,
                                    width: '1%'
                                  }}
                                />
                              ))}
                            </div>
                          )}
                        </div>

                        {/* Waveform silence and filter markers - only show if enabled in processing options */}
                        <div className="absolute inset-0 flex items-center px-0 z-20">
                          {segments.length > 0 &&
                            segments.map((segment, idx) => {
                              const left = (segment.start_ms / (duration * 1000)) * 100;
                              const width = ((segment.end_ms - segment.start_ms) / (duration * 1000)) * 100;
                              const isSilence = segment.type === "silence";
                              const isFiller = segment.type === "filler";

                              // Only show markers for segments that will be processed
                              if (isSilence && !shouldProcessSilence) return null;
                              if (isFiller && !shouldProcessFillerWords) return null;
                              if (!isSilence && !isFiller) return null;

                              return (
                                <div
                                  key={idx}
                                  className={cn(
                                    "absolute h-full rounded transition-colors",
                                    isSilence && "bg-red-500/30 border-x border-red-500/50",
                                    isFiller && "bg-blue-500/30 border-x border-blue-500/50 pointer-events-auto cursor-help"
                                  )}
                                  title={isFiller && segment.filler_word ? `"${segment.filler_word}"` : undefined}
                                  style={{ left: `${left}%`, width: `${width}%` }}
                                />
                              );
                            })}
                        </div>

                        {/* Time markers */}
                        <div className="absolute bottom-0 left-0 right-0 h-4 flex justify-between px-2 pointer-events-none">
                          {(() => {
                            const markerCount = Math.max(5, Math.floor(5 * zoomLevel));
                            return [...Array(markerCount + 1)].map((_, i) => {
                              const timeAtMarker = (i / markerCount) * duration;
                              return (
                                <div key={i} className="flex flex-col items-center">
                                  <div className="w-px h-1 bg-border" />
                                  <span className="text-[8px] text-muted-foreground">
                                    {formatDurationMs(timeAtMarker * 1000)}
                                  </span>
                                </div>
                              );
                            });
                          })()}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Controls */}
              <div className="flex flex-col md:flex-row justify-between items-center gap-4 mt-4">
                <div className="flex items-center gap-4 order-2 md:order-1">
                  <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground" onClick={skipBackward}>
                    <SkipBack className="h-6 w-6" />
                  </Button>
                  <Button
                    onClick={togglePlayPause}
                    className="w-12 h-12 rounded-2xl"
                    disabled={!videoStreamUrl}
                  >
                    {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
                  </Button>
                  <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground" onClick={skipForward}>
                    <SkipForward className="h-6 w-6" />
                  </Button>

                  <div className="h-8 w-px bg-border mx-2" />

                  <div className="flex items-center bg-muted rounded-lg p-1 border border-border">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={() => setZoomLevel(Math.max(0.5, zoomLevel - 0.25))}
                    >
                      <ZoomOut className="h-4 w-4" />
                    </Button>

                    {/* Custom progress bar showing zoom level */}
                    <div className="relative w-20 h-2 bg-border rounded-lg mx-2 cursor-pointer" onClick={(e) => {
                      const rect = e.currentTarget.getBoundingClientRect();
                      const x = e.clientX - rect.left;
                      const percentage = x / rect.width;
                      const newZoom = 0.5 + (percentage * 3.5); // 0.5 to 4 range
                      setZoomLevel(Math.round(newZoom * 4) / 4); // Round to nearest 0.25
                    }}>
                      <div
                        className="absolute top-0 left-0 h-full bg-primary rounded-lg transition-all duration-200"
                        style={{ width: `${((zoomLevel - 0.5) / 3.5) * 100}%` }}
                      />
                      {/* Progress indicator circle */}
                      <div
                        className="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-primary rounded-full border-2 border-background shadow-sm transition-all duration-200"
                        style={{ left: `${((zoomLevel - 0.5) / 3.5) * 100}%`, transform: 'translate(-50%, 0%)' }}
                      />
                      {/* Invisible range input for accessibility */}
                      <input
                        type="range"
                        min="0.5"
                        max="4"
                        step="0.25"
                        value={zoomLevel}
                        onChange={(e) => setZoomLevel(parseFloat(e.target.value))}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      />
                    </div>

                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={() => setZoomLevel(Math.min(4, zoomLevel + 0.25))}
                    >
                      <ZoomIn className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="flex gap-3 order-1 md:order-2 w-full md:w-auto items-center">
                  <div className="text-xs text-muted-foreground flex items-center gap-3">
                    {shouldProcessSilence && silenceCount > 0 && (
                      <span className="flex items-center gap-1.5">
                        <div className="w-2 h-2 rounded-sm bg-red-500/50 ring-1 ring-red-500" />
                        {silenceCount} silence
                      </span>
                    )}
                    {shouldProcessFillerWords && fillerCount > 0 && (
                      <span className="flex items-center gap-1.5">
                        <div className="w-2 h-2 rounded-sm bg-blue-500/50 ring-1 ring-blue-500" />
                        {fillerCount} filler
                      </span>
                    )}
                    {/* {segmentsToProcess > 0 && (
                      <span className="text-foreground font-medium">
                        = {segmentsToProcess} to remove
                      </span>
                    )} */}
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          /* Processed Tab Content */
          <div className="flex-1 min-h-0 flex flex-col gap-6">
            {hasProcessedVideo ? (
              <>
                {/* Processed Video Preview */}
                <div className="flex justify-center relative bg-black/40 rounded-2xl border border-primary/30 overflow-hidden max-h-[45vh] lg:max-h-[50vh] xl:max-h-[60vh]">
                  <div className="relative h-full aspect-video bg-black shadow-2xl flex items-center justify-center">
                    <video
                      ref={processedVideoRef}
                      src={processedVideoStreamUrl}
                      className="w-full h-full object-contain"
                      controls
                    />
                  </div>
                </div>

                {/* Processed Video Info */}
                <div className="bg-card border border-border rounded-2xl p-5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                        <Scissors className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="text-base font-semibold text-foreground">Processed Video</h3>
                        <p className="text-sm text-muted-foreground">
                          {processedMediaFile?.original_filename} • {processedMediaFile?.duration_seconds?.toFixed(1)}s
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">
                        Original: {duration.toFixed(1)}s → Processed: {processedMediaFile?.duration_seconds?.toFixed(1)}s
                      </p>
                      <p className="text-sm text-primary font-medium">
                        {((1 - (processedMediaFile?.duration_seconds || 0) / duration) * 100).toFixed(1)}% reduced
                      </p>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              /* No Processed Video Placeholder */
              <div className="flex-1 min-h-0 flex items-center justify-center bg-muted/30 rounded-2xl border border-dashed border-border">
                <div className="text-center p-8">
                  <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                    <Scissors className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">No Processed Video Yet</h3>
                  <p className="text-sm text-muted-foreground mb-4 max-w-md">
                    Go to the Original tab and click &quot;Process Video&quot; to remove silence from your video.
                  </p>
                  <Button onClick={() => setActiveTab("original")}>
                    Go to Original
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
