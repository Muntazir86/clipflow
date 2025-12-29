# ClipFlow Docker Deployment

This guide explains how to deploy the complete ClipFlow application (frontend + backend) using Docker.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Git

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd clipflow
   ```

2. **Set up environment variables:**

   **Backend (.env):**
   Copy `apps/api/.env.example` to `apps/api/.env` and configure:
   ```bash
   cp apps/api/.env.example apps/api/.env
   ```

   Edit the .env file with your settings:
   ```env
   # Database
   POSTGRES_USER=clipflow
   POSTGRES_PASSWORD=clipflow
   POSTGRES_DB=clipflow
   DATABASE_URL=postgresql://clipflow:clipflow@clipflow-postgres:5432/clipflow

   # Redis
   REDIS_URL=redis://clipflow-redis:6379/0

   # JWT
   SECRET_KEY=your-super-secret-jwt-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # CORS (for Docker deployment)
   CORS_ORIGINS=http://localhost:3000,http://clipflow-web:3000

   # Storage
   STORAGE_TYPE=local
   UPLOAD_DIR=/app/uploads

   # AI Features (optional)
   AI_FEATURES_ENABLED=false
   OPENAI_API_KEY=your-openai-key-if-using-ai-features
   ```

   **Frontend Environment:**
   Create `apps/web/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

3. **Build and run:**
   ```bash
   # Development (with hot reload)
   docker-compose up --build

   # Production
   docker-compose --profile production up --build -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5434
   - Redis: localhost:6389

## Services

### Frontend (clipflow-web)
- **Port:** 3000
- **Framework:** Next.js 16 with App Router
- **Features:** Responsive UI, video player, project management

### Backend API (clipflow-api)
- **Port:** 8000
- **Framework:** FastAPI
- **Features:** REST API, file uploads, AI processing

### Database (clipflow-postgres)
- **Port:** 5434 (external), 5432 (internal)
- **Image:** PostgreSQL 15 Alpine

### Cache/Queue (clipflow-redis)
- **Port:** 6389 (external), 6379 (internal)
- **Image:** Redis 7 Alpine

### Background Tasks (celery-worker, celery-beat)
- **Purpose:** Audio processing, file cleanup

### Reverse Proxy (nginx) - Production Only
- **Ports:** 80, 443
- **Features:** Load balancing, SSL termination, static file caching

## Development Workflow

### Running Individual Services

```bash
# Only backend
docker-compose up clipflow-api clipflow-postgres clipflow-redis

# Only frontend
docker-compose up clipflow-web

# Only database
docker-compose up clipflow-postgres
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f clipflow-api
```

### Database Management

```bash
# Access database
docker-compose exec clipflow-postgres psql -U clipflow -d clipflow

# Run migrations
docker-compose exec clipflow-api alembic upgrade head
```

### File Storage

Uploaded files are stored in the `uploads` Docker volume. To persist data:

```bash
# Backup uploads
docker run --rm -v clipflow_uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads-backup.tar.gz -C /data .
```

## Production Deployment

For production deployment:

1. **Enable nginx profile:**
   ```bash
   docker-compose --profile production up -d
   ```

2. **Configure SSL:**
   - Place SSL certificates in `./ssl/` directory
   - Uncomment SSL server block in `nginx.conf`

3. **Environment Variables:**
   - Use strong secrets for JWT and NextAuth
   - Configure proper CORS origins
   - Set up external database if needed

4. **Monitoring:**
   - Health checks are configured for all services
   - Check logs: `docker-compose logs -f`

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Change ports in `docker-compose.yml` if needed

2. **Database connection issues:**
   - Ensure PostgreSQL is healthy: `docker-compose ps`
   - Check logs: `docker-compose logs clipflow-postgres`

3. **File upload issues:**
   - Check upload directory permissions
   - Verify volume mounting: `docker volume ls`

4. **CORS errors:**
   - Verify `CORS_ORIGINS` in backend .env
   - Check nginx configuration for API proxy

### Reset Everything

```bash
# Stop and remove all containers, volumes, networks
docker-compose down -v --remove-orphans

# Clean up images (optional)
docker system prune -f
```

## Architecture

```
Internet
    ↓
  Nginx (80/443)
    ↓
┌─────────────┐    ┌─────────────┐
│ clipflow-web│    │ clipflow-api│
│   (3000)    │    │   (8000)    │
└─────────────┘    └─────────────┘
         ↓               ↓
    ┌─────────────┐ ┌─────────────┐
    │ clipflow-db │ │ clipflow-redis│
    │   (5432)    │ │    (6379)    │
    └─────────────┘ └─────────────┘
                        ↓
                  ┌─────────────┐
                  │celery-worker│
                  └─────────────┘
```

This setup provides a complete, production-ready deployment of ClipFlow with proper service isolation, health checks, and scalability.
