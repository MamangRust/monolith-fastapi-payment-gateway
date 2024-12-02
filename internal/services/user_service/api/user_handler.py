from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List
from prometheus_client import Counter, Histogram
from domain.dtos.request.user import CreateUserRequest, UpdateUserRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.service.user import IUserService
from domain.dtos.response.user import UserResponse
from infrastructure.service.user import UserService
from lib.security.header import token_security
from infrastructure.di import get_user_service

# Prometheus metrics for user service
REQUEST_COUNT = Counter('user_service_requests_count', 'Total number of requests received', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('user_service_request_duration_seconds', 'Duration of request handling', ['method', 'endpoint'])

router = APIRouter()

@router.get("", response_model=ApiResponse[List[UserResponse]])
async def get_users(
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Get a list of all users."""
    method = 'GET'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await user_service.get_users()
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=500, detail="Failed to retrieve users")
            return response
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving users"
        )


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user_by_id(
    user_id: int,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Get a user by their ID."""
    method = 'GET'
    endpoint = f'/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await user_service.find_by_id(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail="User not found")
            return response
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving the user"
        )


@router.post("", response_model=ApiResponse[UserResponse])
async def create_user(
    user_request: CreateUserRequest,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Create a new user."""
    method = 'POST'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await user_service.create_user(user_request)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail="Failed to create user")
            return response
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the user"
        )


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
    user_id: int,
    user_request: UpdateUserRequest,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Update an existing user's information."""
    method = 'PUT'
    endpoint = f'/{user_id}'
    try:
        user_request.id = user_id  # Assign user_id from the path parameter to the request body
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await user_service.update_user(user_request)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail="Failed to update user")
            return response
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the user"
        )


@router.delete("/{user_id}", response_model=ApiResponse[None])
async def delete_user(
    user_id: int,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Delete a user by their ID."""
    method = 'DELETE'
    endpoint = f'/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await user_service.delete_user(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail="User not found")
            return response
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the user"
        )
