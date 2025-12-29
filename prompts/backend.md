# ClipFlow API - Backend Development Prompt

## Project Overview
Build a FastAPI backend service for a video editing web application that analyzes audio tracks to detect speech segments, silence, and optionally filler words. The service processes uploaded audio, returns timestamp data for the frontend to display, and does NOT handle video cutting (that happens client-side).

---

## Tech Stack
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT tokens with refresh token rotation
- **Task Queue:** Celery with Redis (for async audio processing)
- **Audio Processing:** FFmpeg, pydub
- **Voice Detection:** Silero VAD (default), OpenAI Whisper API (optional)
- **File Storage:** Local filesystem (dev) / S3-compatible storage (prod)
- **Containerization:** Docker + Docker Compose

---

## Environment Configuration

Create a comprehensive `.env` configuration system:
```env
# Application
APP_NAME=clipflow-api
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here
API_VERSION=v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/videocut

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# File Storage
STORAGE_TYPE=local  # local | s3
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=500
ALLOWED_EXTENSIONS=mp4,webm,mov,avi,mkv,mp3,wav,m4a

# S3 Configuration (if STORAGE_TYPE=s3)
S3_BUCKET_NAME=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_REGION=
S3_ENDPOINT_URL=

# AI Features Toggle
AI_FEATURES_ENABLED=false  # Master switch for AI features
WHISPER_API_ENABLED=false  # Enable OpenAI Whisper for transcription
OPENAI_API_KEY=your-openai-api-key

# Processing Configuration
DEFAULT_PROCESSING_MODE=vad  # vad | whisper
VAD_AGGRESSIVENESS=3  # 1-3, higher = more aggressive silence detection
MIN_SILENCE_DURATION_MS=300
MIN_SPEECH_DURATION_MS=250
SILENCE_THRESHOLD_DB=-40

# Filler Words Configuration (only used when WHISPER_API_ENABLED=true)
DETECT_FILLER_WORDS=true
FILLER_WORDS=um,uh,like,you know,basically,actually,literally,so,well,I mean
FILLER_WORD_PADDING_MS=100  # Padding around detected filler words

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600  # seconds
```

---

## Database Schema

### Users Table
```
users:
  - id: UUID (primary key)
  - email: String (unique, indexed)
  - password_hash: String
  - full_name: String (nullable)
  - is_active: Boolean (default: true)
  - is_verified: Boolean (default: false)
  - created_at: DateTime
  - updated_at: DateTime
  - last_login: DateTime (nullable)
  - settings: JSONB (user preferences)
```

### Projects Table
```
projects:
  - id: UUID (primary key)
  - user_id: UUID (foreign key -> users)
  - name: String
  - description: String (nullable)
  - status: Enum (created, processing, completed, failed)
  - created_at: DateTime
  - updated_at: DateTime
```

### Media Files Table
```
media_files:
  - id: UUID (primary key)
  - project_id: UUID (foreign key -> projects)
  - original_filename: String
  - stored_filename: String
  - file_path: String
  - file_size: BigInteger
  - mime_type: String
  - duration_seconds: Float
  - created_at: DateTime
```

### Analysis Results Table
```
analysis_results:
  - id: UUID (primary key)
  - media_file_id: UUID (foreign key -> media_files)
  - processing_mode: Enum (vad, whisper)
  - status: Enum (pending, processing, completed, failed)
  - segments: JSONB  # Array of segment data
  - transcription: Text (nullable, only for whisper mode)
  - filler_words_detected: JSONB (nullable)
  - processing_time_ms: Integer
  - error_message: String (nullable)
  - created_at: DateTime
  - completed_at: DateTime (nullable)
```

### Refresh Tokens Table
```
refresh_tokens:
  - id: UUID (primary key)
  - user_id: UUID (foreign key -> users)
  - token_hash: String (indexed)
  - expires_at: DateTime
  - created_at: DateTime
  - revoked: Boolean (default: false)
  - revoked_at: DateTime (nullable)
```

---

## API Endpoints

### Authentication Endpoints
```
POST /api/v1/auth/register
- Request: { email, password, full_name? }
- Response: { user, access_token, refresh_token }
- Validation: Email format, password strength (min 8 chars, 1 uppercase, 1 number)

POST /api/v1/auth/login
- Request: { email, password }
- Response: { user, access_token, refresh_token }
- Set refresh token as HTTP-only cookie as well

POST /api/v1/auth/refresh
- Request: { refresh_token } or from HTTP-only cookie
- Response: { access_token, refresh_token }
- Implement token rotation (invalidate old refresh token)

POST /api/v1/auth/logout
- Headers: Authorization: Bearer <access_token>
- Revoke refresh token, clear cookies
- Response: { message: "Logged out successfully" }

POST /api/v1/auth/forgot-password
- Request: { email }
- Response: { message } (always success to prevent enumeration)
- Send reset email with token

POST /api/v1/auth/reset-password
- Request: { token, new_password }
- Response: { message }

GET /api/v1/auth/me
- Headers: Authorization: Bearer <access_token>
- Response: { user object }

PATCH /api/v1/auth/me
- Headers: Authorization: Bearer <access_token>
- Request: { full_name?, settings? }
- Response: { updated user }
```

### Project Endpoints
```
GET /api/v1/projects
- Headers: Authorization: Bearer <access_token>
- Query: ?page=1&limit=20&status=completed
- Response: { projects[], pagination }

POST /api/v1/projects
- Headers: Authorization: Bearer <access_token>
- Request: { name, description? }
- Response: { project }

GET /api/v1/projects/{project_id}
- Response: { project with media_files and analysis_results }

PATCH /api/v1/projects/{project_id}
- Request: { name?, description? }
- Response: { updated project }

DELETE /api/v1/projects/{project_id}
- Soft delete or hard delete with file cleanup
- Response: { message }
```

### Media Upload Endpoints
```
POST /api/v1/projects/{project_id}/upload
- Headers: Authorization: Bearer <access_token>
- Body: multipart/form-data with video/audio file
- Validate file size, extension, mime type
- Extract duration using FFprobe
- Response: { media_file, upload_url? }

POST /api/v1/upload/presigned
- For large files, generate presigned URL for direct S3 upload
- Request: { filename, content_type, file_size }
- Response: { upload_url, file_id }

POST /api/v1/upload/confirm/{file_id}
- Confirm upload completed for presigned URL flow
- Response: { media_file }
```

### Analysis Endpoints
```
POST /api/v1/media/{media_id}/analyze
- Headers: Authorization: Bearer <access_token>
- Request: {
    processing_mode?: "vad" | "whisper" | "auto",  # auto uses env default
    vad_aggressiveness?: 1-3,
    min_silence_duration_ms?: number,
    min_speech_duration_ms?: number,
    detect_filler_words?: boolean,  # only if whisper enabled
    custom_filler_words?: string[]  # additional filler words
  }
- If whisper requested but AI_FEATURES_ENABLED=false, return error
- Response: { analysis_id, status: "processing" }
- Trigger Celery task for background processing

GET /api/v1/analysis/{analysis_id}
- Response: { analysis_result with segments }

GET /api/v1/analysis/{analysis_id}/status
- Lightweight status check for polling
- Response: { status, progress_percent?, error_message? }

GET /api/v1/media/{media_id}/waveform
- Generate and return waveform data for visualization
- Response: { peaks: number[], duration: number, sample_rate: number }
```

### Configuration Endpoints
```
GET /api/v1/config/features
- Public endpoint, no auth required
- Response: {
    ai_features_enabled: boolean,
    whisper_available: boolean,
    filler_detection_available: boolean,
    max_file_size_mb: number,
    allowed_extensions: string[],
    default_processing_mode: string
  }
```

---

## Core Processing Logic

### Audio Extraction Service
```
1. Accept video file path
2. Use FFmpeg to extract audio track
3. Convert to WAV format (16kHz mono for optimal VAD performance)
4. Store extracted audio temporarily
5. Return audio file path and metadata
```

### VAD Processing Service (Default - No AI)
```
1. Load audio file
2. Initialize Silero VAD model (runs locally, no API)
3. Process audio in chunks
4. For each chunk, determine speech probability
5. Apply thresholds and minimum duration filters
6. Merge adjacent speech segments
7. Return segments array:
   [
     {
       start_ms: number,
       end_ms: number,
       type: "speech" | "silence",
       confidence: number
     }
   ]
```

### Whisper Processing Service (AI-Enabled)
```
1. Check AI_FEATURES_ENABLED and WHISPER_API_ENABLED flags
2. If disabled, throw appropriate error
3. Load audio file
4. Call OpenAI Whisper API with:
   - model: "whisper-1"
   - response_format: "verbose_json"
   - timestamp_granularities: ["word", "segment"]
5. Parse response to get word-level timestamps
6. Run VAD in parallel for silence detection
7. Analyze transcription for filler words:
   - Match against configured FILLER_WORDS list
   - Consider context (word at start of sentence vs middle)
8. Merge VAD segments with transcription data
9. Return enhanced segments:
   [
     {
       start_ms: number,
       end_ms: number,
       type: "speech" | "silence" | "filler",
       confidence: number,
       text?: string,  # transcribed text for this segment
       filler_word?: string  # if type is "filler"
     }
   ]
```

### Segment Post-Processing
```
1. Apply minimum duration filters
2. Merge segments that are too close together
3. Add padding to speech segments (configurable)
4. Calculate suggested "keep" and "remove" classifications:
   - keep: speech segments
   - remove: silence segments
   - suggest_remove: filler word segments (user confirms)
5. Generate edit decision list (EDL) compatible format
```

---

## Celery Tasks

### Task: process_audio_analysis
```python
@celery.task(bind=True, max_retries=3)
def process_audio_analysis(self, analysis_id: str, options: dict):
    """
    Main processing task
    1. Update status to "processing"
    2. Extract audio from video
    3. Generate waveform data
    4. Run VAD or Whisper based on options
    5. Post-process segments
    6. Store results in database
    7. Update status to "completed"
    8. Cleanup temporary files
    
    On failure:
    - Update status to "failed"
    - Store error message
    - Retry with exponential backoff
    """
```

### Task: cleanup_expired_files
```python
@celery.task
def cleanup_expired_files():
    """
    Periodic task (run daily)
    - Delete uploaded files older than X days
    - Delete orphaned analysis results
    - Clear temporary processing files
    """
```

---

## Error Handling

Implement consistent error responses:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": {
      "field": "specific error"
    }
  }
}
```

Error codes:
- VALIDATION_ERROR (400)
- UNAUTHORIZED (401)
- FORBIDDEN (403)
- NOT_FOUND (404)
- FILE_TOO_LARGE (413)
- UNSUPPORTED_FORMAT (415)
- RATE_LIMITED (429)
- AI_FEATURES_DISABLED (403) - when AI requested but disabled
- PROCESSING_FAILED (500)
- EXTERNAL_API_ERROR (502) - Whisper API failures

---

## Security Requirements

1. **Authentication:**
   - Hash passwords with bcrypt (cost factor 12)
   - JWT tokens with short expiry (30 min)
   - Refresh token rotation on each use
   - Revoke all tokens on password change

2. **File Upload Security:**
   - Validate file magic bytes, not just extension
   - Scan for malicious content
   - Generate random filenames for storage
   - Never expose internal file paths

3. **Rate Limiting:**
   - Global rate limit per IP
   - Per-user rate limits for authenticated requests
   - Stricter limits for processing endpoints

4. **Input Validation:**
   - Use Pydantic models for all inputs
   - Sanitize filenames
   - Validate UUIDs format

---

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py  # Dependencies (get_current_user, etc.)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── media.py
│   │   │   ├── analysis.py
│   │   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── media.py
│   │   └── analysis.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── project.py
│   │   ├── media.py
│   │   └── analysis.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── audio_extractor.py
│   │   ├── vad_processor.py
│   │   ├── whisper_processor.py
│   │   ├── segment_processor.py
│   │   ├── waveform_generator.py
│   │   └── storage_service.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   └── analysis_tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       ├── file_utils.py
│       └── ffmpeg_utils.py
├── alembic/
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_projects.py
│   └── test_analysis.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## Docker Configuration

Provide Docker Compose with:
- FastAPI app service
- PostgreSQL database
- Redis for Celery broker/cache
- Celery worker service
- Celery beat for scheduled tasks (optional)

Include health checks for all services.

---

## Testing Requirements

1. Unit tests for all services
2. Integration tests for API endpoints
3. Test both VAD and Whisper processing paths
4. Test AI feature toggle behavior
5. Mock external APIs (Whisper) in tests
6. Minimum 80% code coverage

---

## Documentation

1. OpenAPI/Swagger documentation (auto-generated)
2. README with setup instructions
3. Environment variables documentation
4. API usage examples
5. Deployment guide