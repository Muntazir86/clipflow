# ClipFlow API

A FastAPI backend service for video editing that analyzes audio tracks to detect speech segments, silence, and optionally filler words.

## Features

- **Audio Analysis**: Detect speech and silence segments using Silero VAD
- **AI-Powered Transcription**: Optional OpenAI Whisper integration for transcription and filler word detection
- **Project Management**: Organize media files into projects
- **Async Processing**: Background task processing with Celery
- **JWT Authentication**: Secure authentication with token rotation
- **File Storage**: Local filesystem or S3-compatible storage

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis
- **Audio Processing**: FFmpeg, Silero VAD
- **AI Features**: OpenAI Whisper API (optional)

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- FFmpeg

### Local Development

1. **Clone and setup environment**:
   ```bash
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Setup database**:
   ```bash
   # Start PostgreSQL and Redis
   # Then run migrations
   alembic upgrade head
   ```

4. **Run the application**:
   ```bash
   # Start API server
   uvicorn app.main:app --reload

   # In another terminal, start Celery worker
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

5. **Access the API**:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

```bash
docker-compose up -d
```

This starts:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Celery worker
- Celery beat (scheduled tasks)

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh tokens |
| POST | `/api/v1/auth/logout` | Logout |
| GET | `/api/v1/auth/me` | Get current user |
| PATCH | `/api/v1/auth/me` | Update profile |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | List projects |
| POST | `/api/v1/projects` | Create project |
| GET | `/api/v1/projects/{id}` | Get project |
| PATCH | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |

### Media
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/projects/{id}/upload` | Upload media file |
| GET | `/api/v1/media/{id}/waveform` | Get waveform data |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analysis/media/{id}/analyze` | Start analysis |
| GET | `/api/v1/analysis/{id}` | Get analysis result |
| GET | `/api/v1/analysis/{id}/status` | Get analysis status |

### Configuration
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/config/features` | Get available features |

## Environment Variables

See `.env.example` for all available configuration options.

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | - |
| `REDIS_URL` | Redis connection URL | - |
| `JWT_SECRET_KEY` | Secret for JWT tokens | - |
| `AI_FEATURES_ENABLED` | Enable AI features | `false` |
| `WHISPER_API_ENABLED` | Enable Whisper API | `false` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `STORAGE_TYPE` | `local` or `s3` | `local` |

## Processing Modes

### VAD Mode (Default)
Uses Silero VAD for local voice activity detection. No API calls required.

```json
{
  "processing_mode": "vad",
  "vad_aggressiveness": 3,
  "min_silence_duration_ms": 300,
  "min_speech_duration_ms": 250
}
```

### Whisper Mode (AI-Enabled)
Uses OpenAI Whisper API for transcription and filler word detection.

```json
{
  "processing_mode": "whisper",
  "detect_filler_words": true,
  "custom_filler_words": ["um", "uh"]
}
```

## Analysis Response Format

```json
{
  "id": "uuid",
  "status": "completed",
  "segments": [
    {
      "start_ms": 0,
      "end_ms": 5000,
      "type": "speech",
      "confidence": 0.95,
      "text": "Hello world",
      "classification": "keep"
    },
    {
      "start_ms": 5000,
      "end_ms": 6000,
      "type": "silence",
      "confidence": 0.9,
      "classification": "remove"
    }
  ],
  "processing_time_ms": 1234
}
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## Project Structure

```
apps/api/
├── app/
│   ├── api/
│   │   ├── deps.py          # Dependencies
│   │   └── v1/              # API v1 endpoints
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── tasks/               # Celery tasks
│   ├── utils/               # Utilities
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   └── main.py              # FastAPI app
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── docker-compose.yml       # Docker setup
├── Dockerfile               # Container build
└── requirements.txt         # Dependencies
```

## License

MIT
