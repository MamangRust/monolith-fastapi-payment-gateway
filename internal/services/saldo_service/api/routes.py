from fastapi import APIRouter
from api import saldo_handler

router = APIRouter()


router.include_router(
    router=saldo_handler.router, tags=["Saldo"], prefix="/saldo"
)