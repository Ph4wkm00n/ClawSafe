from fastapi import APIRouter
from fastapi.responses import Response

from app.services.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
async def prometheus_metrics():
    return Response(content=get_metrics(), media_type="text/plain; charset=utf-8")
