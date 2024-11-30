from fastapi import APIRouter
from internal.services.tranfer_service.api import transfer_handler

router = APIRouter()


router.include_router(
    router=transfer_handler.router, tags=["Transfer"], prefix="/transfer"
)