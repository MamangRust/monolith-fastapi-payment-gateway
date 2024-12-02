from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from lib.security.header import token_security
from domain.request.transfer import CreateTransferRequest, UpdateTransferRequest


router = APIRouter()

transfer_client = HttpClient(base_url="http://transfer-service:8004/api")


@router.get("/")
async def get_transfers(
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.get(
            "/transfer", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred: ",
        )


@router.get("/{id}")
async def get_transfer(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.get(
            f"/transfer/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving transfer {id}: ",
        )


@router.get("/user/{user_id}")
async def get_transfer_user(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.get(
            f"/transfer/user/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving transfer for user {user_id}: ",
        )


@router.get("/transfer/{user_id}")
async def get_transfer_users(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.get(
            f"/transfer/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving transfers for user {user_id}: ",
        )


@router.post("/")
async def create_transfer(
    input: CreateTransferRequest,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.post(
            "/transfer", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while creating transfer: ",
        )


@router.put("/{id}")
async def update_transfer(
    id: int,
    input: UpdateTransferRequest,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.put(
            f"/transfer/{id}", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while updating transfer {id}: ",
        )


@router.delete("/{id}")
async def delete_transfer(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await transfer_client.delete(
            f"/transfer/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while deleting transfer {id}: ",
        )
