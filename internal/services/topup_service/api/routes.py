from fastapi import APIRouter
from api import topup_handler

router = APIRouter()


router.include_router(
    router=topup_handler.router, tags=["Topup"], prefix="/topup"
)