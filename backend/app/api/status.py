from fastapi import APIRouter, HTTPException

from app.models.schemas import CategoryName, CategoryStatus, OverallStatus
from app.services.policy import get_active_policy
from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

router = APIRouter()


async def _get_status() -> OverallStatus:
    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()

    # Load active policy for scoring adjustments
    policy_data = None
    try:
        policy_resp = await get_active_policy()
        if policy_resp:
            policy_data = policy_resp.config.model_dump()
    except Exception:
        pass  # Score without policy if loading fails

    return compute_status(findings, policy=policy_data)


@router.get("/status", response_model=OverallStatus)
async def get_overall_status():
    return await _get_status()


@router.get("/status/{category}", response_model=CategoryStatus)
async def get_category_status(category: CategoryName):
    status = await _get_status()
    for cat in status.categories:
        if cat.category == category:
            return cat
    raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
