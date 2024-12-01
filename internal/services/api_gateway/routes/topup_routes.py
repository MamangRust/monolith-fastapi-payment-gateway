from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from lib.security.header import token_security
from domain.request.topup import CreateTopupRequest, UpdateTopupRequest


router = APIRouter()

topup_client = HttpClient(base_url="http://topup-service:8003/api")


@router.get("/")
async def get_topups(
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.get(
            "/topup", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred: {e.message} - {e.details}",
        )


@router.get("/{id}")
async def get_topup(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.get(
            f"/topup/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving topup {id}: {e.message} - {e.details}",
        )


@router.get("/user/{user_id}")
async def get_topup_user(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.get(
            f"/topup/user/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving transfer for user {user_id}: {e.message} - {e.details}",
        )


@router.get("/users/{user_id}")
async def get_topup_users(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.get(
            f"/topup/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving transfers for user {user_id}: {e.message} - {e.details}",
        )


@router.post("/")
async def create_topup(
    input: CreateTopupRequest,
    token: str = Depends(token_security),
):
    headers = await get_auth_headers(token)
    try:
        response = await topup_client.post(
            "/topup", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while creating topup: {e.message} - {e.details}",
        )


@router.put("/{id}")
async def update_topup(
    id: int,
    input: UpdateTopupRequest,
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.put(
            f"/topup/{id}", json=input.model_dump(), headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while updating topup {id}: {e.message} - {e.details}",
        )


@router.delete("/{id}")
async def delete_topup(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await topup_client.delete(
            f"/topup/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while deleting topup {id}: {e.message} - {e.details}",
        )
