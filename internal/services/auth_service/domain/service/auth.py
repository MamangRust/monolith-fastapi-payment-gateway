import abc
from typing import List, Optional, Any, Union
from internal.services.auth_service.domain.dtos.response.api import ApiResponse, ErrorResponse
from internal.services.auth_service.domain.dtos.response.user import UserResponse
from internal.services.auth_service.domain.dtos.request.auth import RegisterRequest, LoginRequest


class IAuthService(abc.ABC):
    @staticmethod
    async def register_user(self, request: RegisterRequest) -> Union[ApiResponse[UserResponse], ErrorResponse]: ...

    @staticmethod
    async def login_user(self, request: LoginRequest) -> Union[ApiResponse[str], ErrorResponse]: ...