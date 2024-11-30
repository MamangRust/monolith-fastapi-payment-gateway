from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger
from typing import Union, List

from internal.services.user_service.domain.repository.user import IUserRepository
from internal.services.user_service.domain.service.user import IUserService

from internal.lib.security.hash_password import Hashing

from internal.services.user_service.domain.dtos.request.user import (
    CreateUserRequest,
    UpdateUserRequest,
)
from internal.services.user_service.domain.dtos.response.api import (
    ApiResponse,
    ErrorResponse,
)
from internal.lib.utils.errors import AppError
from internal.services.user_service.domain.dtos.response.user import UserResponse


from internal.lib.otel.otel_config import OpenTelemetryManager

logger = get_logger()

class UserService(IUserService):
    def __init__(
        self,
        repository: IUserRepository,
        hashing: Hashing,
        kafka_manager: KafkaManager,
        otel_manager: OpenTelemetryManager,
    ) -> None:
        self.repository = repository
        self.hashing = hashing
        self.otel_manager = otel_manager

    async def get_users(self) -> Union[ApiResponse[List[UserResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Users") as span:
            try:
                users = await self.repository.find_all()
                user_responses = [UserResponse.from_dto(user) for user in users]
                return ApiResponse(
                    status="success",
                    message="Successfully retrieved users.",
                    data=user_responses,
                )
            except Exception as e:
                logger.error("Error retrieving users", error=str(e))
                span.record_exception(e)
                span.set_attribute("error", "Internal Server Error")
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )

    async def find_by_id(
        self, id: int
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Find User by ID") as span:
            span.set_attribute("user_id", id)
            try:
                user = await self.repository.find_by_id(id)
                if not user:
                    span.set_attribute("error", "User not found")
                    return ErrorResponse(
                        status="error",
                        message="User with the specified ID does not exist.",
                    )
                return ApiResponse(
                    status="success",
                    message="Successfully retrieved user.",
                    data=UserResponse.from_dto(user),
                )
            except Exception as e:
                logger.error("Error retrieving user by ID", user_id=id, error=str(e))
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )

    async def create_user(
        self, input: CreateUserRequest
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Create User") as span:
            span.set_attribute("email", input.email)
            try:
                exists = await self.repository.find_by_email_exists(email=input.email)
                if exists:
                    logger.error("Email already exists", email=input.email)
                    span.set_attribute("error", "Email already exists")
                    return ErrorResponse(
                        status="error",
                        message="Email already exists.",
                    )

                hashed_password = await self.hashing.hash_password(input.password)
                input.password = hashed_password

                user = await self.repository.create_user(input)
                return ApiResponse(
                    status="success",
                    message="User created successfully.",
                    data=UserResponse.from_dtos(user),
                )
            except Exception as e:
                logger.error("Error creating user", error=str(e))
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )

    async def update_user(
        self, input: UpdateUserRequest
    ) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Update User") as span:
            span.set_attribute("user_id", input.user_id)
            try:
                user = await self.repository.find_by_id(input.user_id)
                if not user:
                    span.set_attribute("error", "User not found")
                    return ErrorResponse(
                        status="error",
                        message="User with the specified ID does not exist.",
                    )

                updated_user = await self.repository.update_user(input)
                return ApiResponse(
                    status="success",
                    message="User updated successfully.",
                    data=UserResponse.from_dto(updated_user),
                )
            except Exception as e:
                logger.error("Error updating user", user_id=input.user_id, error=str(e))
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )

    async def delete_user(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        with self.otel_manager.start_trace("Delete User") as span:
            span.set_attribute("user_id", id)
            try:
                user = await self.repository.find_by_id(id)
                if not user:
                    span.set_attribute("error", "User not found")
                    return ErrorResponse(
                        status="error",
                        message="User with the specified ID does not exist.",
                    )

                await self.repository.delete_user(id)
                return ApiResponse(
                    status="success",
                    message="User deleted successfully.",
                    data=None,
                )
            except Exception as e:
                logger.error("Error deleting user", user_id=id, error=str(e))
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )
