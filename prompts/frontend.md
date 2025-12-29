# ClipFlow - Frontend Development Prompt

## Project Overview
Build a React-based web application for video editing that allows users to upload videos, view AI-analyzed audio segments on a timeline, adjust segment boundaries, and export edited videos. All video cutting/exporting happens client-side using FFmpeg.wasm to avoid server load and reduce costs.

---

## Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS + shadcn/ui components
- **State Management:** Zustand
- **Data Fetching:** TanStack Query (React Query)
- **Video Processing:** FFmpeg.wasm
- **Waveform/Timeline:** wavesurfer.js with regions plugin
- **Forms:** React Hook Form + Zod validation
- **Authentication:** JWT with HTTP-only cookies + memory storage

---

## Environment Configuration
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=VideoCut

# Feature Flags (fetched from API but can override)
NEXT_PUBLIC_MAX_FILE_SIZE_MB=500

# FFmpeg Configuration
NEXT_PUBLIC_FFMPEG_CORE_URL=/ffmpeg/ffmpeg-core.js  # Self-hosted
# Or use CDN: https://unpkg.com/@ffmpeg/core@0.12.4/dist/ffmpeg-core.js
```

---

## Application Routes
```
/                       # Landing page (public)
/login                  # Login page
/register               # Registration page
/forgot-password        # Password reset request
/reset-password         # Password reset form (with token)

/dashboard              # User's projects list (protected)
/projects/new           # Create new project (protected)
/projects/[id]          # Project detail/editor (protected)
/projects/[id]/export   # Export progress page (protected)

/settings               # User settings (protected)
/settings/account       # Account settings
/settings/preferences   # App preferences
```

---

## Core Components Architecture

### Layout Components
```
RootLayout
├── AuthProvider (context for auth state)
├── QueryProvider (TanStack Query)
├── ThemeProvider (dark/light mode)
└── ToastProvider (notifications)

DashboardLayout (for protected routes)
├── Sidebar
│   ├── Logo
│   ├── Navigation
│   └── UserMenu
├── Header
│   ├── Breadcrumbs
│   └── Actions
└── MainContent
```

### Authentication Components
```
LoginForm
- Email input with validation
- Password input with show/hide toggle
- Remember me checkbox
- Submit button with loading state
- Link to register/forgot password

RegisterForm
- Full name input
- Email input with validation
- Password input with strength indicator
- Confirm password
- Terms acceptance checkbox
- Submit button

ForgotPasswordForm
ResetPasswordForm
```

### Dashboard Components
```
ProjectsGrid
├── ProjectCard
│   ├── Thumbnail (first frame or placeholder)
│   ├── Project name
│   ├── Status badge (processing/completed/failed)
│   ├── Created date
│   ├── Duration
│   └── Actions dropdown (open, delete, duplicate)
├── NewProjectCard (dashed border, + icon)
└── EmptyState (when no projects)

ProjectFilters
├── Search input
├── Status filter dropdown
└── Sort dropdown (date, name)

Pagination
```

### Editor Components (Main Feature)
```
VideoEditor (main container)
├── EditorHeader
│   ├── BackButton
│   ├── ProjectName (editable)
│   ├── ProcessingStatus
│   └── ExportButton
│
├── EditorMain
│   ├── VideoPreviewSection
│   │   ├── VideoPlayer
│   │   │   - HTML5 video element
│   │   │   - Custom controls
│   │   │   - Current time display
│   │   │   - Play/pause, seek
│   │   │   - Volume control
│   │   │   - Playback speed
│   │   │   - Fullscreen toggle
│   │   └── PreviewToggle (original vs edited preview)
│   │
│   └── SegmentDetails (sidebar)
│       ├── CurrentSegmentInfo
│       │   - Start/end time (editable)
│       │   - Duration
│       │   - Type (speech/silence/filler)
│       │   - Transcription text (if available)
│       │   - Keep/Remove toggle
│       └── SegmentStats
│           - Total duration
│           - Removed duration
│           - Estimated output duration
│
├── TimelineSection
│   ├── TimelineToolbar
│   │   ├── ZoomControls (+/- buttons, slider)
│   │   ├── SelectionTools
│   │   │   - Select all speech
│   │   │   - Select all silence
│   │   │   - Select all fillers
│   │   │   - Invert selection
│   │   └── UndoRedo buttons
│   │
│   ├── WaveformTimeline
│   │   ├── TimeRuler (timestamps)
│   │   ├── Waveform (wavesurfer.js)
│   │   ├── SegmentRegions (colored overlays)
│   │   │   - Green: keep (speech)
│   │   │   - Red: remove (silence)
│   │   │   - Yellow: suggested remove (filler)
│   │   ├── DraggableHandles (on region edges)
│   │   ├── PlayheadIndicator
│   │   └── HoverPreview
│   │
│   └── SegmentList (below waveform)
│       - Scrollable list of all segments
│       - Click to jump to segment
│       - Toggle keep/remove
│       - Shows transcription preview
│
└── EditorFooter
    ├── ProcessingModeIndicator (VAD vs AI)
    ├── KeyboardShortcutsHelp
    └── ReprocessButton
```

### Export Components
```
ExportModal
├── ExportSettings
│   ├── OutputFormat (mp4, webm, mov)
│   ├── QualityPreset (low, medium, high, original)
│   ├── Resolution (keep original, 1080p, 720p, 480p)
│   └── Advanced options toggle
│       ├── Video codec
│       ├── Audio codec
│       ├── Bitrate
│       └── Frame rate
├── ExportPreview
│   - Estimated file size
│   - Estimated duration
│   - Segments to include count
└── ExportActions
    ├── Cancel button
    └── Export button

ExportProgress
├── ProgressBar (with percentage)
├── CurrentStep (extracting, processing, encoding)
├── TimeRemaining estimate
├── Cancel button
└── On completion:
    ├── Download button
    ├── Preview button
    └── Share options
```

### Upload Components
```
FileUpload
├── DropZone
│   ├── Drag & drop area
│   ├── File input trigger
│   ├── Supported formats list
│   └── Max file size indicator
├── UploadProgress
│   ├── File name
│   ├── Progress bar
│   ├── Upload speed
│   └── Cancel button
└── UploadError
    ├── Error message
    └── Retry button

ProcessingOptions (shown after upload)
├── ProcessingModeSelect
│   ├── "Fast" (VAD only) - always available
│   └── "AI Enhanced" (Whisper) - if enabled
├── FillerWordsToggle (if AI mode)
├── CustomFillerWords input (if AI mode)
├── SensitivitySlider
└── StartProcessingButton
```

---

## State Management (Zustand Stores)

### Auth Store
```typescript
interface AuthStore {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  updateUser: (data: Partial<User>) => void;
  checkAuth: () => Promise<void>;
}
```

### Editor Store
```typescript
interface EditorStore {
  // Project state
  project: Project | null;
  mediaFile: MediaFile | null;
  analysisResult: AnalysisResult | null;
  
  // Timeline state
  segments: Segment[];
  selectedSegmentId: string | null;
  playheadPosition: number;
  zoomLevel: number;
  isPlaying: boolean;
  
  // History for undo/redo
  history: EditorState[];
  historyIndex: number;
  
  // Actions
  setSegments: (segments: Segment[]) => void;
  updateSegment: (id: string, updates: Partial<Segment>) => void;
  toggleSegmentKeep: (id: string) => void;
  splitSegment: (id: string, atTime: number) => void;
  mergeSegments: (ids: string[]) => void;
  selectSegment: (id: string | null) => void;
  setPlayheadPosition: (time: number) => void;
  setZoomLevel: (level: number) => void;
  
  // Bulk actions
  keepAllSpeech: () => void;
  removeAllSilence: () => void;
  removeAllFillers: () => void;
  invertSelection: () => void;
  
  // History actions
  undo: () => void;
  redo: () => void;
  canUndo: boolean;
  canRedo: boolean;
  
  // Export
  getExportSegments: () => Segment[];  // Only segments marked as "keep"
}
```

### FFmpeg Store
```typescript
interface FFmpegStore {
  isLoaded: boolean;
  isLoading: boolean;
  loadError: string | null;
  
  // Export state
  isExporting: boolean;
  exportProgress: number;
  exportStep: 'idle' | 'preparing' | 'cutting' | 'encoding' | 'finalizing';
  exportError: string | null;
  
  // Actions
  loadFFmpeg: () => Promise<void>;
  exportVideo: (
    inputFile: File,
    segments: Segment[],
    options: ExportOptions
  ) => Promise<Blob>;
  cancelExport: () => void;
}
```

### UI Store
```typescript
interface UIStore {
  sidebarOpen: boolean;
  activeModal: string | null;
  theme: 'light' | 'dark' | 'system';
  
  toggleSidebar: () => void;
  openModal: (modalId: string) => void;
  closeModal: () => void;
  setTheme: (theme: Theme) => void;
}
```

---

## FFmpeg.wasm Integration

### Setup and Loading
```
1. Load FFmpeg.wasm core on app initialization (lazy load)
2. Show loading indicator during initialization
3. Cache loaded state to avoid reloading
4. Handle loading failures gracefully
5. Check browser compatibility (SharedArrayBuffer required)
   - Show warning if not supported
   - Provide instructions for enabling cross-origin isolation
```

### Video Export Process
```
1. Read input video file into FFmpeg virtual filesystem
2. Generate filter_complex command for segment cutting:
   - Use 'select' filter for video segments
   - Use 'aselect' filter for audio segments
   - Concatenate selected segments
3. Apply output settings (codec, quality, resolution)
4. Monitor progress via FFmpeg logs
5. Read output file from virtual filesystem
6. Create blob URL for download
7. Cleanup virtual filesystem
```

### Export Command Generation
```
For segments: [{start: 0, end: 5, keep: true}, {start: 8, end: 15, keep: true}]

Generate:
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]select='between(t,0,5)+between(t,8,15)',setpts=N/FRAME_RATE/TB[v]; \
                   [0:a]aselect='between(t,0,5)+between(t,8,15)',asetpts=N/SR/TB[a]" \
  -map "[v]" -map "[a]" \
  output.mp4
```

---

## Wavesurfer.js Integration

### Configuration
```javascript
const wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: '#4a5568',
  progressColor: '#3182ce',
  cursorColor: '#e53e3e',
  cursorWidth: 2,
  height: 128,
  normalize: true,
  partialRender: true,  // For performance with long files
  plugins: [
    RegionsPlugin.create({
      dragSelection: false,  // We create regions from API data
    }),
    TimelinePlugin.create({
      container: '#timeline',
    }),
  ],
});
```

### Region Management
```
1. Receive segments from API
2. Convert segments to wavesurfer regions:
   - id: segment.id
   - start: segment.start_ms / 1000
   - end: segment.end_ms / 1000
   - color: based on segment.type and keep status
   - drag: true (allow moving)
   - resize: true (allow resizing via handles)
   
3. Listen to region events:
   - region-updated: sync with store
   - region-clicked: select segment
   - region-in: highlight in list
   
4. Sync playhead with video player
5. Handle zoom via wavesurfer.zoom()
```

---

## Video Player Integration

### Sync Requirements
```
1. Video player currentTime syncs with wavesurfer playhead
2. Clicking on waveform seeks video
3. Video play/pause controls waveform
4. Keyboard shortcuts work globally:
   - Space: play/pause
   - Left/Right arrows: seek ±5s
   - J/K/L: playback speed control
   - [ / ]: jump to prev/next segment
   
5. Preview mode:
   - Toggle between "original" and "edited" preview
   - Edited preview skips removed segments
```

---

## API Integration (TanStack Query)

### Query Keys Structure
```typescript
const queryKeys = {
  auth: {
    me: ['auth', 'me'],
  },
  projects: {
    all: ['projects'],
    list: (filters) => ['projects', 'list', filters],
    detail: (id) => ['projects', 'detail', id],
  },
  media: {
    detail: (id) => ['media', 'detail', id],
    waveform: (id) => ['media', 'waveform', id],
  },
  analysis: {
    detail: (id) => ['analysis', 'detail', id],
    status: (id) => ['analysis', 'status', id],
  },
  config: {
    features: ['config', 'features'],
  },
};
```

### Key Queries/Mutations
```typescript
// Fetch feature flags on app load
useQuery({
  queryKey: queryKeys.config.features,
  queryFn: () => api.get('/config/features'),
  staleTime: Infinity,  // Rarely changes
});

// Poll analysis status while processing
useQuery({
  queryKey: queryKeys.analysis.status(analysisId),
  queryFn: () => api.get(`/analysis/${analysisId}/status`),
  refetchInterval: (data) => 
    data?.status === 'processing' ? 2000 : false,
});

// Upload with progress
useMutation({
  mutationFn: (file: File) => uploadWithProgress(file, onProgress),
  onSuccess: (data) => {
    queryClient.invalidateQueries(queryKeys.projects.all);
  },
});
```

---

## Keyboard Shortcuts
```
Global (when in editor):
- Space: Play/Pause
- Ctrl/Cmd + S: Save project
- Ctrl/Cmd + E: Open export modal
- Ctrl/Cmd + Z: Undo
- Ctrl/Cmd + Shift + Z: Redo
- Escape: Deselect segment / Close modal

Playback:
- Left Arrow: Seek back 5s
- Right Arrow: Seek forward 5s
- Shift + Left: Seek back 1s
- Shift + Right: Seek forward 1s
- J: Slow down playback
- K: Pause
- L: Speed up playback
- Home: Go to start
- End: Go to end

Timeline:
- [ : Jump to previous segment
- ] : Jump to next segment
- Delete/Backspace: Toggle current segment to "remove"
- Enter: Toggle current segment to "keep"
- Ctrl/Cmd + A: Select all segments
- +/=: Zoom in
- -: Zoom out
- 0: Reset zoom

Segment editing:
- S: Split segment at playhead
- M: Merge selected segments
```

---

## Responsive Design

### Breakpoints
```
- Mobile: < 768px (limited functionality, upload + view only)
- Tablet: 768px - 1024px (simplified editor)
- Desktop: > 1024px (full editor)
```

### Mobile Considerations
```
- Hide timeline on mobile, show segment list instead
- Simplified video player controls
- Disable FFmpeg export (too resource-intensive)
- Show message: "For full editing, use desktop"
- Allow viewing projects and basic playback
```

---

## Error Handling

### Error Boundaries
```
1. Root error boundary - catches catastrophic failures
2. Editor error boundary - catches editor-specific issues
3. FFmpeg error boundary - handles WASM failures
```

### User-Friendly Errors
```
- File too large → "File exceeds maximum size of X MB"
- Unsupported format → "This format isn't supported. Try MP4, WebM, or MOV"
- Processing failed → "Analysis failed. Please try again or use a different video"
- FFmpeg error → "Export failed. Your browser may not support this feature"
- Network error → "Connection lost. Retrying..." (with auto-retry)
```

---

## Loading States
```
PageLoader: Full page spinner for route transitions
EditorSkeleton: Skeleton UI while loading project
WaveformLoader: Loading indicator over waveform area
SegmentListLoader: Skeleton list items
ExportLoader: Full screen overlay with progress
```

---

## Accessibility Requirements

1. All interactive elements keyboard accessible
2. Focus management in modals
3. Aria labels on all buttons/controls
4. Screen reader announcements for:
   - Upload progress
   - Processing status
   - Export progress
5. Color contrast compliance (WCAG AA)
6. Reduced motion support
7. Skip to main content link

---

## Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── projects/
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── settings/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── ui/  # shadcn components
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── editor/
│   │   │   ├── VideoPlayer.tsx
│   │   │   ├── Timeline.tsx
│   │   │   ├── Waveform.tsx
│   │   │   ├── SegmentRegion.tsx
│   │   │   ├── SegmentList.tsx
│   │   │   ├── SegmentDetails.tsx
│   │   │   ├── TimelineToolbar.tsx
│   │   │   └── EditorHeader.tsx
│   │   ├── upload/
│   │   ├── export/
│   │   └── common/
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useProjects.ts
│   │   ├── useEditor.ts
│   │   ├── useFFmpeg.ts
│   │   ├── useWavesurfer.ts
│   │   ├── useKeyboardShortcuts.ts
│   │   └── useMediaQuery.ts
│   │
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── editorStore.ts
│   │   ├── ffmpegStore.ts
│   │   └── uiStore.ts
│   │
│   ├── lib/
│   │   ├── api.ts  # Axios instance with interceptors
│   │   ├── ffmpeg.ts  # FFmpeg.wasm utilities
│   │   ├── queryClient.ts
│   │   └── utils.ts
│   │
│   ├── types/
│   │   ├── api.ts
│   │   ├── editor.ts
│   │   └── index.ts
│   │
│   └── constants/
│       ├── routes.ts
│       ├── keyboard.ts
│       └── colors.ts
│
├── public/
│   ├── ffmpeg/  # Self-hosted FFmpeg.wasm core files
│   └── ...
│
├── next.config.js  # Configure headers for SharedArrayBuffer
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── README.md
```

---

## Next.js Configuration

### Headers for FFmpeg.wasm
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin',
          },
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'require-corp',
          },
        ],
      },
    ];
  },
};
```

---

## Testing Requirements

1. Unit tests for stores and utilities
2. Component tests with React Testing Library
3. E2E tests with Playwright for critical flows:
   - Registration/Login
   - Upload video
   - Wait for processing
   - Adjust segments
   - Export video
4. Visual regression tests for editor UI

---

## Performance Optimizations

1. Lazy load FFmpeg.wasm only when entering editor
2. Virtual scrolling for segment list (long videos)
3. Debounce segment updates to API
4. Waveform partial rendering for long files
5. Image optimization for thumbnails
6. Code splitting by route
7. Service worker for offline asset caching