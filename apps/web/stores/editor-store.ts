import { create } from "zustand";
import type {
  ProjectWithMediaResponse,
  MediaFileWithAnalysisResponse,
  AnalysisResponse,
  SegmentResponse,
} from "@/types/api";

export interface EditorSegment extends SegmentResponse {
  id: string;
  keep: boolean;
}

interface EditorState {
  project: ProjectWithMediaResponse | null;
  mediaFile: MediaFileWithAnalysisResponse | null;
  analysisResult: AnalysisResponse | null;
  segments: EditorSegment[];
  selectedSegmentId: string | null;
  playheadPosition: number;
  zoomLevel: number;
  isPlaying: boolean;
  history: EditorSegment[][];
  historyIndex: number;
}

interface EditorActions {
  setProject: (project: ProjectWithMediaResponse | null) => void;
  setMediaFile: (mediaFile: MediaFileWithAnalysisResponse | null) => void;
  setAnalysisResult: (result: AnalysisResponse | null) => void;
  setSegments: (segments: EditorSegment[]) => void;
  updateSegment: (id: string, updates: Partial<EditorSegment>) => void;
  toggleSegmentKeep: (id: string) => void;
  selectSegment: (id: string | null) => void;
  setPlayheadPosition: (time: number) => void;
  setZoomLevel: (level: number) => void;
  setIsPlaying: (playing: boolean) => void;
  keepAllSpeech: () => void;
  removeAllSilence: () => void;
  removeAllFillers: () => void;
  invertSelection: () => void;
  undo: () => void;
  redo: () => void;
  getExportSegments: () => EditorSegment[];
  reset: () => void;
}

type EditorStore = EditorState & EditorActions;

const initialState: EditorState = {
  project: null,
  mediaFile: null,
  analysisResult: null,
  segments: [],
  selectedSegmentId: null,
  playheadPosition: 0,
  zoomLevel: 1,
  isPlaying: false,
  history: [],
  historyIndex: -1,
};

function generateSegmentId(segment: SegmentResponse, index: number): string {
  return `${segment.type}-${segment.start_ms}-${segment.end_ms}-${index}`;
}

export const useEditorStore = create<EditorStore>((set, get) => ({
  ...initialState,

  setProject: (project) => set({ project }),

  setMediaFile: (mediaFile) => set({ mediaFile }),

  setAnalysisResult: (result) => {
    if (result?.segments) {
      const segments: EditorSegment[] = result.segments.map((seg, idx) => ({
        ...seg,
        id: generateSegmentId(seg, idx),
        keep: seg.type === "speech",
      }));
      set({ analysisResult: result, segments, history: [segments], historyIndex: 0 });
    } else {
      set({ analysisResult: result });
    }
  },

  setSegments: (segments) => {
    const { history, historyIndex } = get();
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(segments);
    set({ segments, history: newHistory, historyIndex: newHistory.length - 1 });
  },

  updateSegment: (id, updates) => {
    const segments = get().segments.map((seg) =>
      seg.id === id ? { ...seg, ...updates } : seg
    );
    get().setSegments(segments);
  },

  toggleSegmentKeep: (id) => {
    const segments = get().segments.map((seg) =>
      seg.id === id ? { ...seg, keep: !seg.keep } : seg
    );
    get().setSegments(segments);
  },

  selectSegment: (id) => set({ selectedSegmentId: id }),

  setPlayheadPosition: (time) => set({ playheadPosition: time }),

  setZoomLevel: (level) => set({ zoomLevel: Math.max(0.5, Math.min(10, level)) }),

  setIsPlaying: (playing) => set({ isPlaying: playing }),

  keepAllSpeech: () => {
    const segments = get().segments.map((seg) => ({
      ...seg,
      keep: seg.type === "speech" ? true : seg.keep,
    }));
    get().setSegments(segments);
  },

  removeAllSilence: () => {
    const segments = get().segments.map((seg) => ({
      ...seg,
      keep: seg.type === "silence" ? false : seg.keep,
    }));
    get().setSegments(segments);
  },

  removeAllFillers: () => {
    const segments = get().segments.map((seg) => ({
      ...seg,
      keep: seg.type === "filler" ? false : seg.keep,
    }));
    get().setSegments(segments);
  },

  invertSelection: () => {
    const segments = get().segments.map((seg) => ({
      ...seg,
      keep: !seg.keep,
    }));
    get().setSegments(segments);
  },

  undo: () => {
    const { history, historyIndex } = get();
    if (historyIndex > 0) {
      set({
        segments: history[historyIndex - 1],
        historyIndex: historyIndex - 1,
      });
    }
  },

  redo: () => {
    const { history, historyIndex } = get();
    if (historyIndex < history.length - 1) {
      set({
        segments: history[historyIndex + 1],
        historyIndex: historyIndex + 1,
      });
    }
  },

  getExportSegments: () => get().segments.filter((seg) => seg.keep),

  reset: () => set(initialState),
}));
