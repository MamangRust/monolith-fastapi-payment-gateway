from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from domain.request.auth import RegisterRequest, LoginRequest


router = APIRouter()

auth_client = HttpClient(base_url="http://auth-service:8001")


@router.post("/register")
async def register_user(request: RegisterRequest):
    try:
        response = await auth_client.post("/auth/register", json=request)
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail={
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/login")
async def login_user(request: LoginRequest):
    try:
        response = await auth_client.post("/auth/login", json=request)
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail={
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

