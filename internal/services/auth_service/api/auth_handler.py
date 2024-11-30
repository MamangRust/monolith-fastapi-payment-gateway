from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from internal.services.auth_service.domain.dtos.request.auth import RegisterRequest, LoginRequest
from internal.services.auth_service.domain.dtos.response.api import ApiResponse, ErrorResponse
from internal.services.auth_service.domain.dtos.response.user import UserResponse
from internal.services.auth_service.infrastructure.service.auth import AuthService

from internal.services.auth_service.infrastructure.di import get_auth_service

router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserResponse])
async def register_user(
    request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    try:
        user = await auth_service.register_user(request)

        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail="Failed to create user")

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")

@router.post("/login", response_model=ApiResponse[str])
async def login_user(
    request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.login_user(request)
        
        if isinstance(user, ErrorResponse):
            raise HTTPException(status_code=404, detail="User not found or login failed")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during login")
