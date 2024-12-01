from fastapi import APIRouter
from api import withdraw_handler

router = APIRouter()


router.include_router(
    router=withdraw_handler.router, tags=["Withdraw"], prefix="/withdraw"
)