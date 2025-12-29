# ClipFlow Frontend Development Plan

## Overview
Build a Next.js 16 web application for video editing with AI-powered audio analysis. The app allows users to upload videos, view analyzed audio segments on a timeline, adjust segment boundaries, and export edited videos using FFmpeg.wasm.

---

## Tech Stack
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **State Management**: Zustand
- **Data Fetching**: TanStack Query
- **Forms**: React Hook Form + Zod
- **Icons**: Material Symbols (as per UI designs)
- **Video Processing**: FFmpeg.wasm (future)
- **Waveform**: wavesurfer.js (future)

---

## Color Theme (from UI designs)
```css
--primary: #39E079 (Green)
--background-light: #f6f8f7
--background-dark: #122017
--card-dark: #181b21
--border-dark: #282e39
--surface-dark: #1c2e24
--text-muted: #9da6b9
```

---

## Screens to Build

### 1. Landing Page (`/`)
**Purpose**: Marketing page to attract users
**Key Features**:
- Hero section with headline "Cut the Noise, Keep the Privacy"
- Feature cards (Smart Silence Removal, Text-Based Editing, Local-First Privacy)
- Pricing section (Free, Pro Creator, Studio)
- Footer with links
**API Integration**: None (static page)

---

### 2. Login Page (`/login`)
**Purpose**: User authentication
**Key Features**:
- Email/password form with validation
- Password visibility toggle
- "Forgot password?" link
- Social login buttons (Google, Apple) - UI only
- Link to registration
- Decorative visual panel on right side
**API Integration**:
- `POST /api/v1/auth/login` → `LoginRequest` → `TokenResponse`

---

### 3. Registration Page (`/register`)
**Purpose**: New user signup
**Key Features**:
- Full name, email, password, confirm password fields
- Password strength indicator
- Terms acceptance checkbox
- Social signup buttons (Google, GitHub) - UI only
- Link to login
- Privacy badge "End-to-end encrypted"
**API Integration**:
- `POST /api/v1/auth/register` → `RegisterRequest` → `TokenResponse`

---

### 4. Dashboard Page (`/dashboard`)
**Purpose**: Project management hub
**Key Features**:
- Sidebar navigation (Dashboard, Projects, AI Tools, Settings)
- Welcome header with user name
- Quick AI Tools grid (Remove Silence, Word Filter, Auto-Subtitles, AI Shorts)
- Recent Projects grid with:
  - Upload new card (drag & drop)
  - Project cards with thumbnail, name, status, duration
  - Processing indicator for active jobs
- Storage usage indicator
- Search bar
**API Integration**:
- `GET /api/v1/auth/me` → `UserResponse`
- `GET /api/v1/projects` → `ProjectListResponse`
- `DELETE /api/v1/projects/{id}` → `MessageResponse`

---

### 5. Project Creation Flow (`/projects/new`)
**Purpose**: Create new project and upload video
**Key Features**:
- Step indicator (Upload → Details & AI → Review)
- Video upload dropzone with progress
- Project name input
- Canvas format selector (16:9, 9:16, 1:1)
- AI Magic Tools toggles:
  - Silence Removal
  - Profanity Filter
  - Auto Captions
- Source video preview card
- Privacy guarantee badge
**API Integration**:
- `POST /api/v1/projects` → `ProjectCreate` → `ProjectResponse`
- `POST /api/v1/projects/{id}/upload` → multipart/form-data → `MediaFileResponse`
- `POST /api/v1/analysis/media/{id}/analyze` → `AnalysisCreate` → `AnalysisStartResponse`

---

### 6. Video Editor Page (`/projects/[id]`)
**Purpose**: Main editing interface
**Key Features**:
- Sidebar navigation
- Header with project name, auto-save indicator, export button
- Video preview with play controls
- Audio timeline with:
  - Waveform visualization
  - Segment regions (speech/silence/filler)
  - Playhead indicator
  - Zoom controls
- Segment legend (Silence, Filtered Words)
- Action buttons (Cut Silence, Filter Words)
- Playback controls (prev, play/pause, next)
**API Integration**:
- `GET /api/v1/projects/{id}` → `ProjectWithMediaResponse`
- `GET /api/v1/media/{id}/waveform` → `WaveformResponse`
- `GET /api/v1/analysis/{id}` → `AnalysisResponse`
- `GET /api/v1/analysis/{id}/status` → `AnalysisStatusResponse` (polling)

---

### 7. Settings Page (`/settings`)
**Purpose**: User preferences
**Key Features**:
- Profile section (name, email)
- Theme toggle (light/dark)
- Account actions
**API Integration**:
- `GET /api/v1/auth/me` → `UserResponse`
- `PATCH /api/v1/auth/me` → `UserUpdate` → `UserResponse`

---

## Project Structure
```
apps/web/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── projects/
│   │   │   ├── new/page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── settings/page.tsx
│   │   └── layout.tsx
│   ├── layout.tsx
│   ├── page.tsx (landing)
│   └── globals.css
├── components/
│   ├── ui/ (Button, Input, Card, etc.)
│   ├── auth/ (LoginForm, RegisterForm)
│   ├── dashboard/ (Sidebar, ProjectCard, etc.)
│   ├── editor/ (VideoPlayer, Timeline, etc.)
│   └── providers/ (QueryProvider, AuthProvider, ThemeProvider)
├── lib/
│   ├── api.ts (API client with axios)
│   ├── auth.ts (token management)
│   └── utils.ts (cn, formatters)
├── stores/
│   ├── auth-store.ts
│   ├── editor-store.ts
│   └── ui-store.ts
├── types/
│   └── api.ts (TypeScript types from OpenAPI)
└── hooks/
    ├── use-auth.ts
    ├── use-projects.ts
    └── use-toast.ts
```

---

## Implementation Order

### Phase 1: Foundation
1. Install dependencies (shadcn/ui approach, zustand, tanstack-query, axios, zod, react-hook-form)
2. Setup Tailwind CSS with custom theme
3. Create base UI components (Button, Input, Card, etc.)
4. Setup API client with interceptors
5. Create TypeScript types from OpenAPI spec
6. Setup Zustand stores (auth, ui)
7. Create providers (Query, Auth, Theme)

### Phase 2: Auth Pages
1. Build auth layout with decorative background
2. Build Login page with form validation
3. Build Register page with form validation
4. Implement auth store with token management

### Phase 3: Dashboard
1. Build dashboard layout with sidebar
2. Build Dashboard page with project grid
3. Implement project CRUD operations
4. Build project cards with status indicators

### Phase 4: Project Creation
1. Build project creation flow
2. Implement file upload with progress
3. Build AI settings panel

### Phase 5: Video Editor
1. Build editor layout
2. Build video player component
3. Build timeline component (placeholder for wavesurfer)
4. Implement segment visualization
5. Connect to analysis API with polling

### Phase 6: Landing & Settings
1. Build landing page
2. Build settings page

---

## API Types Summary (from OpenAPI)

### Auth
- `LoginRequest`: { email, password }
- `RegisterRequest`: { email, password, full_name? }
- `TokenResponse`: { user, access_token, refresh_token, token_type }
- `UserResponse`: { id, email, full_name, is_active, is_verified, created_at, ... }

### Projects
- `ProjectCreate`: { name, description? }
- `ProjectResponse`: { id, user_id, name, description, status, created_at, updated_at }
- `ProjectListResponse`: { projects[], pagination }
- `ProjectStatus`: "created" | "processing" | "completed" | "failed"

### Media
- `MediaFileResponse`: { id, project_id, original_filename, file_size, mime_type, duration_seconds, ... }
- `WaveformResponse`: { peaks[], duration, sample_rate }

### Analysis
- `AnalysisCreate`: { processing_mode?, vad_aggressiveness?, detect_filler_words?, ... }
- `AnalysisResponse`: { id, media_file_id, status, segments[], transcription?, ... }
- `SegmentResponse`: { start_ms, end_ms, type, confidence, text?, filler_word? }
- `AnalysisStatus`: "pending" | "processing" | "completed" | "failed"

### Config
- `FeaturesResponse`: { ai_features_enabled, whisper_available, max_file_size_mb, ... }
