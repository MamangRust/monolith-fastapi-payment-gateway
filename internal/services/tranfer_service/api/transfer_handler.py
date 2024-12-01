from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Optional
from prometheus_client import Counter, Histogram

from internal.services.tranfer_service.domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest
from internal.services.tranfer_service.domain.dtos.response.api import ApiResponse
from internal.services.tranfer_service.domain.service.transfer import ITransferService
from internal.services.tranfer_service.domain.dtos.response.transfer import TransferResponse
from internal.services.tranfer_service.infrastructure.service.transfer import TransferService
from internal.lib.security.header import token_security
from internal.services.tranfer_service.infrastructure.di import get_transfer_service

# Prometheus metrics for transfer service
REQUEST_COUNT = Counter('transfer_service_requests_count', 'Total number of requests received', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('transfer_service_request_duration_seconds', 'Duration of request handling', ['method', 'endpoint'])

router = APIRouter()

@router.get("/", response_model=ApiResponse[List[TransferResponse]])
async def get_transfers(
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all transfers."""
    method = 'GET'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.get_transfers()
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=500, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer by its ID."""
    method = 'GET'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.get_transfer(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer_user(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/user/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.get_transfer_user(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[TransferResponse]]])
async def get_transfer_users(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve all transfers associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/users/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.get_transfer_users(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TransferResponse])
async def create_transfer(
    input: CreateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Create a new transfer."""
    method = 'POST'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.create_transfer(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TransferResponse])
async def update_transfer(
    id: int,
    input: UpdateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Update an existing transfer by its ID."""
    method = 'PUT'
    endpoint = f'/{id}'
    try:
        input.id = id  # Ensure the ID in the path matches the request
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.update_transfer(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Delete a transfer by its ID."""
    method = 'DELETE'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await transfer_service.delete_transfer(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
