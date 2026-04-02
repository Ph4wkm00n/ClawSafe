from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.instance import InstanceCreate, InstanceList, InstanceResponse, InstanceUpdate
from app.models.schemas import BulkFixRequest, BulkFixResponse, InstanceScore
from app.services.instance_manager import (
    bulk_apply_fix,
    create_instance,
    delete_instance,
    get_aggregated_status,
    get_instance,
    get_instance_timeline,
    list_instances,
    update_instance,
)

router = APIRouter()


@router.get("/instances", response_model=InstanceList)
async def get_instances():
    return await list_instances()


@router.post("/instances", response_model=InstanceResponse, dependencies=[Depends(require_auth)])
async def post_instance(data: InstanceCreate):
    return await create_instance(data)


@router.get("/instances/{instance_id}", response_model=InstanceResponse)
async def get_instance_detail(instance_id: str):
    instance = await get_instance(instance_id)
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found.")
    return instance


@router.put("/instances/{instance_id}", response_model=InstanceResponse, dependencies=[Depends(require_auth)])
async def put_instance(instance_id: str, data: InstanceUpdate):
    instance = await update_instance(instance_id, data)
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found.")
    return instance


@router.delete("/instances/{instance_id}", dependencies=[Depends(require_auth)])
async def remove_instance(instance_id: str):
    success = await delete_instance(instance_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete this instance.")
    return {"success": True}


@router.get("/instances/aggregate")
async def aggregate_status():
    """Get cross-instance risk aggregation."""
    return await get_aggregated_status()


@router.get("/instances/{instance_id}/status")
async def get_instance_status(instance_id: str):
    """Get safety status for a specific instance."""
    from app.services.scanner import get_demo_findings, scan_openclaw
    from app.services.scoring import compute_status

    inst = await get_instance(instance_id)
    if inst is None:
        raise HTTPException(status_code=404, detail="Instance not found.")
    findings = scan_openclaw(config_path=inst.config_path)
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    return compute_status(findings)


@router.post("/instances/bulk-fix", response_model=BulkFixResponse, dependencies=[Depends(require_auth)])
async def apply_bulk_fix(req: BulkFixRequest):
    """Apply a fix action to all active instances."""
    results = await bulk_apply_fix(req.action_id)
    succeeded = sum(1 for r in results if r.success)
    return BulkFixResponse(
        results=results,
        total=len(results),
        succeeded=succeeded,
        failed=len(results) - succeeded,
    )


@router.get("/instances/{instance_id}/timeline", response_model=list[InstanceScore])
async def instance_timeline(instance_id: str, days: int = 30):
    """Get risk score timeline for an instance."""
    inst = await get_instance(instance_id)
    if inst is None:
        raise HTTPException(status_code=404, detail="Instance not found.")
    return await get_instance_timeline(instance_id, days)
