from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from lib.security.header import token_security
from domain.request.user import CreateUserRequest, UpdateUserRequest

router = APIRouter()

user_client = HttpClient(base_url="http://user-service:8005/api")


@router.get("/users")
async def get_users(
    token: str = Depends(token_security),
):
    try:
        response = await user_service_client.get(
            "/users", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred: {e.message} - {e.details}",
        )


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await user_service_client.get(
            f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving user {user_id}: {e.message} - {e.details}",
        )


@router.post("/users")
async def create_user(
    user_request: CreateUserRequest,
    token: str = Depends(token_security),
):
    try:
        response = await user_service_client.post(
            "/users", json=user_request.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while creating user: {e.message} - {e.details}",
        )


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_request: UpdateUserRequest,
    token: str = Depends(token_security),
):
    try:
        response = await user_service_client.put(
            f"/users/{user_id}",
            json=user_request.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while updating user {user_id}: {e.message} - {e.details}",
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await user_service_client.delete(
            f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while deleting user {user_id}: {e.message} - {e.details}",
        )
