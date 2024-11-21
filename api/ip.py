from typing import List

from validators.requests_ import IpsDataRequest
from fastapi import APIRouter

ip_router = APIRouter(
    prefix="/ip",
)


@ip_router.post("/process", name="ips-process-endpoint")
async def ips_handler(ips: List[IpsDataRequest]):
    return {"data": ips}
