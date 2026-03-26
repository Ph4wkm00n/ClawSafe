from fastapi import APIRouter

from app.models.schemas import SkillStatusResponse
from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

router = APIRouter()


def _get_current_status():
    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    return compute_status(findings)


@router.get("/skill/status", response_model=SkillStatusResponse)
async def skill_status():
    status = _get_current_status()
    actions = []
    for cat in status.categories:
        if cat.status.value != "safe":
            actions.append(f"{cat.label}: {cat.summary}")

    return SkillStatusResponse(
        summary=status.subtitle,
        status=status.status.value,
        score=status.score,
        top_actions=actions[:3],
    )


@router.get("/skill/actions", response_model=list[str])
async def skill_actions():
    status = _get_current_status()
    actions = []
    for cat in status.categories:
        if cat.status.value != "safe":
            actions.append(f"{cat.action_label} — {cat.summary}")
    return actions[:3]
