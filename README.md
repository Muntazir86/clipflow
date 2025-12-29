# ClipFlow

ClipFlow is a modern video editing platform powered by AI for intelligent audio analysis. It provides seamless video editing capabilities with advanced features like voice activity detection (VAD), speech-to-text transcription, filler word removal, and automated segment classification to help creators produce cleaner, more professional content.

## Features

- **AI-Powered Audio Analysis**: Automatic voice activity detection using Silero VAD
- **Speech Transcription**: Optional OpenAI Whisper integration for accurate transcription
- **Filler Word Detection**: Automatically identify and suggest removal of filler words like "um", "uh", etc.
- **Waveform Visualization**: Interactive waveform display for precise editing
- **Smart Segment Classification**: AI-assisted suggestions for keeping, removing, or reviewing segments
- **Real-time Video Editor**: Web-based timeline editor with drag-and-drop functionality
- **Responsive UI**: Modern, intuitive interface built with Next.js and Tailwind CSS
- **Asynchronous Processing**: Background task processing with Celery and Redis
- **Secure Authentication**: JWT-based auth with refresh token rotation
- **File Storage**: Support for local filesystem or S3-compatible storage

## Tech Stack

### Backend (`apps/api`)
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Queue**: Celery with Redis
- **Audio Processing**: FFmpeg, Silero VAD, OpenAI Whisper
- **Auth**: JWT with bcrypt hashing
- **Storage**: Local filesystem or S3-compatible

### Frontend (`apps/web`)
- **Framework**: Next.js 16 with App Router
- **Styling**: Tailwind CSS v4 with custom theme
- **State Management**: Zustand stores
- **Data Fetching**: TanStack Query
- **Forms**: React Hook Form + Zod validation
- **UI Components**: Radix UI primitives
- **Icons**: Lucide React

### Monorepo Tools
- **Build System**: Turborepo for efficient monorepo management
- **Package Manager**: pnpm (recommended) or npm/yarn
- **TypeScript**: Full TypeScript support across the stack
- **Linting**: ESLint with custom configurations
- **Testing**: pytest for backend, testing-library for frontend

## Prerequisites

Before running ClipFlow, ensure you have the following installed:

- **Docker & Docker Compose**: For containerized database, Redis, and optional backend deployment
- **Node.js 18+**: For frontend development
- **Python 3.11+**: For backend development (optional, can use Docker)
- **FFmpeg**: For audio/video processing
- **Git**: For version control

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/clipflow.git
   cd clipflow
   ```

2. **Install dependencies**:
   ```bash
   # Install monorepo dependencies (pnpm recommended)
   pnpm install

   # Or with npm
   npm install

   # Or with yarn
   yarn install
   ```

3. **Set up environment variables**:
   ```bash
   # Copy environment files
   cp apps/api/.env.example apps/api/.env
   cp apps/web/.env.example apps/web/.env
   ```

   Edit the `.env` files with your configuration:
   - `apps/api/.env`: Database URL, Redis URL, JWT secrets, storage settings, OpenAI API key (optional)
   - `apps/web/.env`: API URL (defaults to `http://localhost:8000/api/v1`)

## Running the Project

### Quick Start (Recommended)

Use Docker Compose for the full stack:

```bash
# Start all services (PostgreSQL, Redis, API, Web)
docker-compose up -d

```

### Run Migrations

```bash
docker exec -w /app clipflow-clipflow-api-1 alembic upgrade head
```

The application will be available at:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Development Setup

1. **Start the backend**:

   Using Docker (recommended):
   ```bash
   # Start database and Redis
   docker-compose up postgres redis -d

   # Run backend in development mode
   cd apps/api
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or locally without Docker:
   ```bash
   cd apps/api
   pip install -r requirements.txt
   # Set up PostgreSQL and Redis manually
   alembic upgrade head
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

2. **Start the frontend**:
   ```bash
   cd apps/web
   pnpm dev
   # Or npm run dev / yarn dev
   ```

3. **Start additional services** (if running locally):
   ```bash
   # In a separate terminal, start Celery worker
   cd apps/api
   celery -A app.tasks.celery_app worker --loglevel=info
   ```

### Monorepo Commands

Use Turborepo for efficient development:

```bash
# Install all dependencies
pnpm install

# Run development servers for all apps
turbo dev

# Build all apps
turbo build

# Run tests
turbo test

# Lint code
turbo lint

# Format code
turbo format
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

Key endpoints:
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/projects` - List user projects
- `POST /api/v1/projects/{id}/upload` - Upload media files
- `POST /api/v1/analysis/media/{id}/analyze` - Start audio analysis
- `GET /api/v1/analysis/{id}` - Get analysis results

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and ensure tests pass
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
