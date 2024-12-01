from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Optional
from prometheus_client import Counter, Histogram

from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest
from domain.dtos.response.api import ApiResponse
from domain.service.withdraw import IWithdrawService
from domain.dtos.response.withdraw import WithdrawResponse
from infrastructure.service.withdraw import WithdrawResponse
from lib.security.header import token_security
from infrastructure.di import get_withdraw_service

# Prometheus metrics
REQUEST_COUNT = Counter('withdraw_service_requests_count', 'Total number of requests received', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('withdraw_service_request_duration_seconds', 'Duration of request handling', ['method', 'endpoint'])

router = APIRouter()

@router.get("/", response_model=ApiResponse[List[WithdrawResponse]])
async def get_withdraws(
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all withdrawal records."""
    method = 'GET'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.get_withdraws()
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=500, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record by its ID."""
    method = 'GET'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.get_withdraw(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/user/{user_id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw_user(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record for a user by user ID."""
    method = 'GET'
    endpoint = f'/user/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.get_withdraw_user(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get(
    "/users/{user_id}", response_model=ApiResponse[Optional[List[WithdrawResponse]]]
)
async def get_withdraw_users(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve all withdrawal records associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/users/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.get_withdraw_users(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/", response_model=ApiResponse[WithdrawResponse])
async def create_withdraw(
    input: CreateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Create a new withdrawal record."""
    method = 'POST'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.create_withdraw(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def update_withdraw(
    id: int,
    input: UpdateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Update an existing withdrawal record."""
    method = 'PUT'
    endpoint = f'/{id}'
    try:
        input.id = id  # Ensure the ID in the path matches the request
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.update_withdraw(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Delete a withdrawal record by its ID."""
    method = 'DELETE'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await withdraw_service.delete_withdraw(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
