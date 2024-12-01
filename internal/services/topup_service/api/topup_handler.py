from fastapi import APIRouter, Depends, HTTPException
from typing import Union, List, Optional

from internal.services.topup_service.domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest

from internal.services.topup_service.domain.dtos.response.api import ApiResponse
from internal.services.topup_service.domain.service.topup import ITopupService
from internal.services.topup_service.domain.dtos.response.topup import TopupResponse

from internal.services.topup_service.infrastructure.service.topup import TopupService

from internal.lib.security.header import token_security
from internal.services.topup_service.infrastructure.di import get_topup_service


router = APIRouter()

REQUEST_COUNT = Counter('topup_service_requests_count', 'Total number of requests received', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('topup_service_request_duration_seconds', 'Duration of request handling', ['method', 'endpoint'])


@router.get("/", response_model=ApiResponse[List[TopupResponse]])
async def get_topups(topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)):
    """Retrieve a list of all topups."""
    method = 'GET'
    endpoint = '/'

    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.get_topups()
            if isinstance(response, ErrorResponse):
                raise HTTPException(status_code=500, detail=response.message)
            return response

    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup(id: int, topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)):
    """Retrieve a single topup by its ID."""
    method = 'GET'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.get_topup(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error' 
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup_user(
    user_id: int, topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)
):
    """Retrieve a single topup associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/user/{user_id}'
    try:
        response = await topup_service.get_topup_user(user_id)
        status = 'success' if not isinstance(response, ErrorResponse) else 'error'
        REQUEST_COUNT.labels(method, endpoint, status).inc()
        if status == 'error':
            raise HTTPException(status_code=404, detail=response.message)
        return response

    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[TopupResponse]]])
async def get_topup_users(
    user_id: int, topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)
):
    """Retrieve all topups associated with a specific user ID."""
    method = 'GET'
    endpoint = f'/users/{user_id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.get_topup_users(user_id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TopupResponse])
async def create_topup(
    input: CreateTopupRequest, topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)
):
    """Create a new topup."""
    method = 'POST'
    endpoint = '/'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.create_topup(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response
    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TopupResponse])
async def update_topup(
    id: int,
    input: UpdateTopupRequest,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str =Depends(token_security)
):
    """Update an existing topup by its ID."""
    method = 'PUT'
    endpoint = f'/{id}'
    try:
        input.id = id  # Ensure the ID in the path matches the request
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.update_topup(input)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=400, detail=response.message)
            return response

    except Exception as e:
        REQUEST_COUNT.labels(method, endpoint, 'error').inc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_topup(id: int, topup_service: ITopupService = Depends(get_topup_service), token: str =Depends(token_security)):
    """Delete a topup by its ID."""
    method = 'DELETE'
    endpoint = f'/{id}'
    try:
        with REQUEST_DURATION.labels(method, endpoint).time():
            response = await topup_service.delete_topup(id)
            status = 'success' if not isinstance(response, ErrorResponse) else 'error'
            REQUEST_COUNT.labels(method, endpoint, status).inc()
            if status == 'error':
                raise HTTPException(status_code=404, detail=response.message)
            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
