import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  UserResponse,
  UserUpdate,
  MessageResponse,
  ProjectCreate,
  ProjectUpdate,
  ProjectResponse,
  ProjectListResponse,
  ProjectWithMediaResponse,
  MediaFileResponse,
  WaveformResponse,
  AnalysisCreate,
  AnalysisResponse,
  AnalysisStartResponse,
  AnalysisStatusResponse,
  FeaturesResponse,
  RefreshTokenRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  ProcessVideoOptions,
} from "@/types/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Token management
let accessToken: string | null = null;
let refreshToken: string | null = null;

export function setTokens(access: string, refresh: string) {
  accessToken = access;
  refreshToken = refresh;
  if (typeof window !== "undefined") {
    localStorage.setItem("refresh_token", refresh);
  }
}

export function getAccessToken() {
  return accessToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
  if (typeof window !== "undefined") {
    localStorage.removeItem("refresh_token");
  }
}

export function loadRefreshToken() {
  if (typeof window !== "undefined") {
    refreshToken = localStorage.getItem("refresh_token");
  }
  return refreshToken;
}

// Request interceptor to add auth header
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (accessToken && config.headers) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    
    if (error.response?.status === 401 && !originalRequest._retry && refreshToken) {
      originalRequest._retry = true;
      
      try {
        const response = await axios.post<TokenResponse>(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        
        setTokens(response.data.access_token, response.data.refresh_token);
        
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
        }
        
        return api(originalRequest);
      } catch {
        clearTokens();
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: (data: RegisterRequest) =>
    api.post<TokenResponse>("/auth/register", data).then((r) => r.data),

  login: (data: LoginRequest) =>
    api.post<TokenResponse>("/auth/login", data).then((r) => r.data),

  refresh: (data: RefreshTokenRequest) =>
    api.post<TokenResponse>("/auth/refresh", data).then((r) => r.data),

  logout: (data: RefreshTokenRequest) =>
    api.post<MessageResponse>("/auth/logout", data).then((r) => r.data),

  forgotPassword: (data: ForgotPasswordRequest) =>
    api.post<MessageResponse>("/auth/forgot-password", data).then((r) => r.data),

  resetPassword: (data: ResetPasswordRequest) =>
    api.post<MessageResponse>("/auth/reset-password", data).then((r) => r.data),

  getMe: () => api.get<UserResponse>("/auth/me").then((r) => r.data),

  updateMe: (data: UserUpdate) =>
    api.patch<UserResponse>("/auth/me", data).then((r) => r.data),
};

// Projects API
export const projectsApi = {
  list: (params?: { page?: number; limit?: number; status?: string }) =>
    api.get<ProjectListResponse>("/projects", { params }).then((r) => r.data),

  get: (id: string) =>
    api.get<ProjectWithMediaResponse>(`/projects/${id}`).then((r) => r.data),

  create: (data: ProjectCreate) =>
    api.post<ProjectResponse>("/projects", data).then((r) => r.data),

  update: (id: string, data: ProjectUpdate) =>
    api.patch<ProjectResponse>(`/projects/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    api.delete<MessageResponse>(`/projects/${id}`).then((r) => r.data),

  uploadMedia: (projectId: string, file: File, onProgress?: (progress: number) => void) => {
    const formData = new FormData();
    formData.append("file", file);

    return api
      .post<MediaFileResponse>(`/media/projects/${projectId}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            onProgress(progress);
          }
        },
      })
      .then((r) => r.data);
  },

  uploadThumbnail: (projectId: string, file: Blob) => {
    const formData = new FormData();
    formData.append("file", file, "thumbnail.jpg");

    return api
      .post<ProjectResponse>(`/projects/${projectId}/thumbnail`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },

  loadThumbnail: async (thumbnailPath: string | null): Promise<string | null> => {
    if (!thumbnailPath) return null;
    thumbnailPath = thumbnailPath.replace("/api/v1", "");
    try {
      const response = await api.get(thumbnailPath, {
        responseType: 'blob',
      });

      const blob = response.data;
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error('Failed to load thumbnail:', error);
      return null;
    }
  },
};

// Media API
export const mediaApi = {
  getWaveform: (mediaId: string) =>
    api.get<WaveformResponse>(`/media/${mediaId}/waveform`).then((r) => r.data),

  getStreamUrl: (mediaId: string) => {
    // const token = localStorage.getItem("access_token");
    return `${API_URL}/media/${mediaId}/stream?token=${accessToken}`;
  },

  processVideo: (mediaId: string, options: ProcessVideoOptions) =>
    api.post<MediaFileResponse>(`/media/${mediaId}/process-video`, options).then((r) => r.data),
};

// Analysis API
export const analysisApi = {
  start: (mediaId: string, data?: AnalysisCreate) =>
    api.post<AnalysisStartResponse>(`/analysis/media/${mediaId}/analyze`, data).then((r) => r.data),

  get: (analysisId: string) =>
    api.get<AnalysisResponse>(`/analysis/${analysisId}`).then((r) => r.data),

  getStatus: (analysisId: string) =>
    api.get<AnalysisStatusResponse>(`/analysis/${analysisId}/status`).then((r) => r.data),
};

// Config API
export const configApi = {
  getFeatures: () => api.get<FeaturesResponse>("/config/features").then((r) => r.data),
};
