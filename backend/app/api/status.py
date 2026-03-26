from fastapi import APIRouter, HTTPException

from app.models.schemas import CategoryName, CategoryStatus, OverallStatus
from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

router = APIRouter()


def _get_status() -> OverallStatus:
    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    return compute_status(findings)


@router.get("/status", response_model=OverallStatus)
async def get_overall_status():
    return _get_status()


@router.get("/status/{category}", response_model=CategoryStatus)
async def get_category_status(category: CategoryName):
    status = _get_status()
    for cat in status.categories:
        if cat.category == category:
            return cat
    raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
