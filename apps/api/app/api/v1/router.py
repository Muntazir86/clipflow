"""API v1 router aggregating all endpoint routers."""

from fastapi import APIRouter

from app.api.v1 import analysis, auth, config, media, projects

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(media.router, prefix="/media", tags=["Media"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(config.router, prefix="/config", tags=["Configuration"])
