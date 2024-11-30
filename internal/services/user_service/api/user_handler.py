from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List
from internal.services.user_service.domain.dtos.request.user import CreateUserRequest, UpdateUserRequest
from internal.services.user_service.domain.dtos.response.api import ApiResponse
from internal.services.user_service.domain.service.user import IUserService
from internal.services.user_service.domain.dtos.response.user import UserResponse
from internal.services.user_service.infrastructure.service.user import UserService

from internal.lib.security.header import token_security
from internal.services.user_service.infrastructure.di import get_user_service

router = APIRouter()




@router.get("", response_model=ApiResponse[List[UserResponse]])
async def get_users(
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Get a list of all users."""
    try:
        response = await user_service.get_users()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail="Failed to retrieve users")
        return response
    except Exception:
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
    try:
        response = await user_service.find_by_id(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail="User not found")
        return response
    except Exception:
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving the user"
        )


@router.post("/", response_model=ApiResponse[UserResponse])
async def create_user(
    user_request: CreateUserRequest,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Create a new user."""
    try:
        response = await user_service.create_user(user_request)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail="Failed to create user")
        return response
    except Exception:
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
    try:
        user_request.id = (
            user_id  # Assign user_id from the path parameter to the request body
        )
        response = await user_service.update_user(user_request)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail="Failed to update user")
        return response
    except Exception:
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
    try:
        response = await user_service.delete_user(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail="User not found")
        return response
    except Exception:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the user"
        )