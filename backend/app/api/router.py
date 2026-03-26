from fastapi import APIRouter

from app.api import (
    activity,
    fixer,
    health,
    notifications,
    policy,
    recommendations,
    scans,
    settings,
    skill,
    status,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(status.router, tags=["status"])
api_router.include_router(recommendations.router, tags=["recommendations"])
api_router.include_router(activity.router, tags=["activity"])
api_router.include_router(settings.router, tags=["settings"])
api_router.include_router(fixer.router, tags=["fixer"])
api_router.include_router(policy.router, tags=["policy"])
api_router.include_router(scans.router, tags=["scans"])
api_router.include_router(notifications.router, tags=["notifications"])
api_router.include_router(skill.router, tags=["skill"])
