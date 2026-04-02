"""API routes for config comparison view."""

from fastapi import APIRouter

from app.models.schemas import ComparisonResponse

router = APIRouter(prefix="/comparison", tags=["comparison"])


@router.get("", response_model=ComparisonResponse)
async def get_comparison():
    from app.services.comparison import get_config_comparison
    return await get_config_comparison()
