from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Optional
from prometheus_client import Counter, Histogram

from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.service.saldo import ISaldoService
from domain.dtos.response.saldo import SaldoResponse

from infrastructure.service.saldo import SaldoService

from lib.security.header import token_security
from infrastructure.di import get_saldo_service

router = APIRouter()



REQUEST_COUNT = Counter('saldo_service_requests_count', 'Total number of requests received', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('saldo_service_request_duration_seconds', 'Duration of request handling', ['method', 'endpoint'])

@router.get("", response_model=ApiResponse[List[SaldoResponse]])
async def get_saldos(
    token: str = Depends(token_security),
    saldo_service: ISaldoService = Depends(get_saldo_service),
):
    """Retrieve a list of all saldos."""
    method = 'GET'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.get_saldos()
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=500, detail=response.message)
            return response

        response = await saldo_service.get_saldos()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)
        return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo by its ID."""
    method = 'GET'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.get_saldo(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo_user(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/user/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.get_saldo_user(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/users/{user_id}", response_model=ApiResponse[Optional[List[SaldoResponse]]]
)
async def get_saldo_users(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve all saldos associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/users/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.get_saldo_users(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response

    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("", response_model=ApiResponse[SaldoResponse])
async def create_saldo(
    input: CreateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Create a new saldo."""
    method = 'POST'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.create_saldo(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def update_saldo(
    id: int,
    input: UpdateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Update an existing saldo by its ID."""
    method = 'PUT'
    endpoint = f'/{id}'
    try:
        input.saldo_id = id  # Ensure the ID in the path matches the request
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.update_saldo(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Delete a saldo by its ID."""
    method = 'DELETE'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await saldo_service.delete_saldo(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response

    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
