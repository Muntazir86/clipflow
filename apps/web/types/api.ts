// Auth Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name?: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

export interface UserResponse {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login: string | null;
  settings: Record<string, unknown> | null;
}

export interface UserUpdate {
  full_name?: string | null;
  settings?: Record<string, unknown> | null;
}

export interface TokenResponse {
  user: UserResponse;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface MessageResponse {
  message: string;
}

// Project Types
export type ProjectStatus = "created" | "processing" | "completed" | "failed";

export interface ProcessingOptions {
  silence_removal: boolean;
  filler_word_filter: boolean;
}

export interface ProjectCreate {
  name: string;
  description?: string | null;
  processing_options?: ProcessingOptions | null;
}

export interface ProjectUpdate {
  name?: string | null;
  description?: string | null;
  status?: ProjectStatus;
}

export interface ProjectResponse {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  status: ProjectStatus;
  thumbnail_url: string | null;
  processing_options: ProcessingOptions | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectWithMediaResponse extends ProjectResponse {
  media_files: MediaFileWithAnalysisResponse[];
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface ProjectListResponse {
  projects: ProjectResponse[];
  pagination: PaginationMeta;
}

// Media Types
export interface ProcessVideoOptions {
  silence_removal: boolean;
  filler_word_filter: boolean;
}

export interface MediaFileResponse {
  id: string;
  project_id: string;
  original_filename: string;
  stored_filename: string;
  file_size: number;
  mime_type: string;
  duration_seconds: number | null;
  created_at: string;
}

export interface MediaFileWithAnalysisResponse {
  id: string;
  original_filename: string;
  file_size: number;
  mime_type: string;
  duration_seconds: number | null;
  created_at: string;
  analysis_results: AnalysisBasicResponse[];
}

export interface AnalysisBasicResponse {
  id: string;
  processing_mode: string;
  status: string;
  created_at: string;
  completed_at: string | null;
}

export interface WaveformResponse {
  peaks: number[];
  duration: number;
  sample_rate: number;
}

// Analysis Types
export type ProcessingMode = "vad" | "whisper";
export type AnalysisStatus = "pending" | "processing" | "completed" | "failed";

export interface AnalysisCreate {
  processing_mode?: "vad" | "whisper" | "auto";
  vad_aggressiveness?: number | null;
  min_silence_duration_ms?: number | null;
  min_speech_duration_ms?: number | null;
  detect_filler_words?: boolean | null;
  custom_filler_words?: string[] | null;
}

export interface SegmentResponse {
  start_ms: number;
  end_ms: number;
  type: "speech" | "silence" | "filler";
  confidence: number;
  text: string | null;
  filler_word: string | null;
}

export interface FillerWordDetection {
  word: string;
  start_ms: number;
  end_ms: number;
  confidence: number;
}

export interface AnalysisResponse {
  id: string;
  media_file_id: string;
  processing_mode: ProcessingMode;
  status: AnalysisStatus;
  segments: SegmentResponse[] | null;
  transcription: string | null;
  filler_words_detected: FillerWordDetection[] | null;
  processing_time_ms: number | null;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface AnalysisStartResponse {
  analysis_id: string;
  status: AnalysisStatus;
}

export interface AnalysisStatusResponse {
  status: AnalysisStatus;
  progress_percent: number | null;
  error_message: string | null;
}

// Config Types
export interface FeaturesResponse {
  // ai_features_enabled: boolean;
  // whisper_available: boolean;
  filler_detection_available: boolean;
  max_file_size_mb: number;
  allowed_extensions: string[];
  default_processing_mode: string;
}

// Error Types
export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}
