from fastapi import APIRouter
from internal.services.api_gateway.routes import auth_routes,  saldo_routes, topup_routes, transfer_routes, withdraw_routes

router = APIRouter()




router.include_router(
    router=auth_routes.router, tags=["Authentication"], prefix="/auth"
)

router.include_router(
    router=saldo_routes.router, tags=["Saldo"], prefix="/saldo"
)

router.include_router(
    router=topup_routes.router, tags=["Topup"], prefix="/topup"
)

router.include_router(
    router=transfer_routes.router, tags=["Transfer"], prefix="/transfer"
)


router.include_router(
    router=withdraw_routes.router, tags=["Withdraw"], prefix="/withdraw"
)