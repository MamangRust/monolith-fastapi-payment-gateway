from fastapi import HTTPException, APIRouter, Depends
from lib.http.http_config import HttpClient, HttpClientError
from lib.security.header import token_security

from domain.request.saldo import CreateSaldoRequest, UpdateSaldoRequest


router = APIRouter()

saldo_client = HttpClient(base_url="http://saldo-service:8002/api")


@router.get("/")
async def get_saldos(
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.get(
            "/saldo", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        print("error : {}".format(e))
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred:",
        )


@router.get("/{id}")
async def get_saldo(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.get(
            f"/saldo/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving saldo {id}: ",
        )


@router.get("/user/{user_id}")
async def get_saldo_user(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.get(
            f"/saldo/user/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving saldo for user {user_id}: ",
        )


@router.get("/users/{user_id}")
async def get_saldo_users(
    user_id: int,
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.get(
            f"/saldo/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while retrieving saldos for user {user_id}: ",
        )


@router.post("/")
async def create_saldo(
    input: CreateSaldoRequest,
    token: str = Depends(token_security),
):

    try:
        response = await saldo_client.post(
            "/saldo",
            json=input.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while creating saldo: ",
        )


@router.put("/{id}")
async def update_saldo(
    id: int,
    input: UpdateSaldoRequest,
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.put(
            f"/saldo/{id}",
            json=input.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while updating saldo {id}: ",
        )


@router.delete("/{id}")
async def delete_saldo(
    id: int,
    token: str = Depends(token_security),
):
    try:
        response = await saldo_client.delete(
            f"/saldo/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except HttpClientError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=f"An error occurred while deleting saldo {id}: ",
        )
