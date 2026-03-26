from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import require_auth
from app.models.instance import InstanceCreate, InstanceList, InstanceResponse, InstanceUpdate
from app.services.instance_manager import (
    create_instance,
    delete_instance,
    get_instance,
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
