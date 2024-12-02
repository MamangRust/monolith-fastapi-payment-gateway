from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from lib.security.header import token_security

from domain.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest


router = APIRouter()

withdraw_client = HttpClient(base_url="http://withdraw-service:8006/api")


@router.get("/")
async def get_withdraws(
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.get(
            "/withdraw", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred: ",
        )


@router.get("/{id}")
async def get_withdraw(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.get(
            f"/withdraw/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving withdraw {id}: ",
        )


@router.get("/user/{user_id}")
async def get_withdraw_user(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.get(
            f"/withdraw/user/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving withdraw for user {user_id}: ",
        )


@router.get("/users/{user_id}")
async def get_withdraw_users(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.get(
            f"/withdraw/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving withdraws for user {user_id}: ",
        )


@router.post("/")
async def create_withdraw(
    input: CreateWithdrawRequest,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.post(
            "/withdraw", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while creating withdraw: ",
        )


@router.put("/{id}")
async def update_withdraw(
    id: int,
    input: UpdateWithdrawRequest,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.put(
            f"/withdraw/{id}", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while updating withdraw {id}: ",
        )


@router.delete("/{id}")
async def delete_withdraw(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await withdraw_client.delete(
            f"/transfer/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while deleting withdraw {id}: ",
        )
