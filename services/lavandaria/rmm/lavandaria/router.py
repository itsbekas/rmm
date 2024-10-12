from fastapi import APIRouter

from rmm.lavandaria.schema import DevicesStatusResponse
from rmm.lavandaria.service import get_device_status

router = APIRouter()


@router.get("/status")
async def get_status() -> DevicesStatusResponse:
    status = get_device_status()
    return status
