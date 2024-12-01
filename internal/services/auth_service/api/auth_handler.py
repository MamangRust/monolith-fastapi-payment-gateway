from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from internal.services.auth_service.domain.dtos.request.auth import RegisterRequest, LoginRequest
from internal.services.auth_service.domain.dtos.response.api import ApiResponse, ErrorResponse
from internal.services.auth_service.domain.dtos.response.user import UserResponse
from internal.services.auth_service.infrastructure.service.auth import AuthService

from internal.services.auth_service.infrastructure.di import get_auth_service
from prometheus_client import Counter, Summary

router = APIRouter()

REGISTER_REQUEST_COUNT = Counter('register_request_count', 'Number of user registration requests')
REGISTER_REQUEST_DURATION = Summary('register_request_duration', 'Time taken for user registration')

LOGIN_REQUEST_COUNT = Counter('login_request_count', 'Number of user login requests')
LOGIN_REQUEST_DURATION = Summary('login_request_duration', 'Time taken for user login')



@router.post("/register", response_model=ApiResponse[UserResponse])
async def register_user(
    request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    REGISTER_REQUEST_COUNT.inc() 

    with REGISTER_REQUEST_DURATION.time(): 
        try:
            user = await auth_service.register_user(request)

            if isinstance(user, ErrorResponse):
                raise HTTPException(status_code=400, detail="Failed to create user")

            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while registering the user")

@router.post("/login", response_model=ApiResponse[str])
async def login_user(
    request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    LOGIN_REQUEST_COUNT.inc()

    with LOGIN_REQUEST_DURATION.time():
        try:
            user = await auth_service.login_user(request)
            
            if isinstance(user, ErrorResponse):
                raise HTTPException(status_code=404, detail="User not found or login failed")
            
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred during login")
