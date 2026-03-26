from fastapi import APIRouter, Depends

from app.core.auth import require_auth
from app.services.container_scanner import get_container_findings, list_containers

router = APIRouter()


@router.get("/vulnerabilities")
async def get_vulnerabilities():
    """Get container and CVE scan results."""
    return get_container_findings()


@router.get("/containers")
async def get_containers():
    """List running Docker containers."""
    return {"containers": list_containers()}


@router.post("/scan/container", dependencies=[Depends(require_auth)])
async def trigger_container_scan():
    """Trigger a container/CVE scan on demand."""
    return get_container_findings()
