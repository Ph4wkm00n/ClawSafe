from fastapi import APIRouter

from app.api import activity, fixer, health, policy, recommendations, settings, status

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(status.router, tags=["status"])
api_router.include_router(recommendations.router, tags=["recommendations"])
api_router.include_router(activity.router, tags=["activity"])
api_router.include_router(settings.router, tags=["settings"])
api_router.include_router(fixer.router, tags=["fixer"])
api_router.include_router(policy.router, tags=["policy"])
