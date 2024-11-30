from internal.services.auth_service.api import auth_handler
from fastapi import APIRouter

router = APIRouter()


router.include_router(
    router=auth_handler.router, tags=['Authentication'], prefix="/auth"
)