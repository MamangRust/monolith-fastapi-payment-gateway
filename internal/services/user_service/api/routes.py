from api import user_handler
from fastapi import APIRouter

router = APIRouter()


router.include_router(
    router=user_handler.router, tags=['Users'], prefix="/users"
)