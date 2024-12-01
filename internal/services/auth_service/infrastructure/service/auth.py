from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger
from typing import Union

from domain.repository.user import IUserRepository
from domain.service.auth import IAuthService

from lib.security.hash_password import Hashing
from lib.security.jwt import JwtConfig

from domain.dtos.request.auth import RegisterRequest, LoginRequest
from domain.dtos.request.user import CreateUserRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.user import UserResponse
from lib.utils.random_vcc import random_vcc
from lib.utils.errors import InvalidCredentialsError
from lib.otel.otel_config import OpenTelemetryManager

logger = get_logger()


class AuthService(IAuthService):
    def __init__(self, repository: IUserRepository, hashing: Hashing, jwt_config: JwtConfig, otel_manager: OpenTelemetryManager):
        self.repository = repository
        self.hashing = hashing
        self.jwt_config = jwt_config
        self.otel_manager = otel_manager

    async def register_user(self, input: RegisterRequest) -> Union[ApiResponse[UserResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Register User") as span:
            span.set_attribute("email", input.email)
            logger.info("Attempting to register user", email=input.email)

            try:
                with self.otel_manager.start_trace("Check Email Existence"):
                    exists = await self.repository.find_by_email_exists(email=input.email)
                    if exists:
                        logger.error("Email already exists", email=input.email)
                        return ErrorResponse(
                            status="error",
                            message="Email already exists.",
                        )

                # Hash password
                with self.otel_manager.start_trace("Hash Password"):
                    hashed_password = await self.hashing.hash_password(input.password)

                # Create user request object
                request = CreateUserRequest(
                    firstname=input.firstname,
                    lastname=input.lastname,
                    email=input.email,
                    password=hashed_password,
                    noc_transfer=random_vcc(),
                    confirm_password=input.confirm_password,
                )

                with self.otel_manager.start_trace("Create User in Repository"):
                    logger.info("Creating user", email=input.email)
                    create_user = await self.repository.create_user(user=request)

                logger.info("User registered successfully", email=input.email)

                return ApiResponse(
                    status="success",
                    message="User registered successfully.",
                    data=UserResponse.from_dto(create_user),
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Unexpected error during registration", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )

    async def login_user(self, input: LoginRequest) -> Union[ApiResponse[str], ErrorResponse]:
        with self.otel_manager.start_trace("Login User") as span:
            span.set_attribute("email", input.email)
            logger.info("Attempting to login user", email=input.email)

            try:
                with self.otel_manager.start_trace("Find User by Email"):
                    user = await self.repository.find_by_email(email=input.email)

                if not user:
                    logger.error("User not found", email=input.email)
                    return ErrorResponse(
                        status="error",
                        message="Invalid credentials.",
                    )

                with self.otel_manager.start_trace("Compare Passwords"):
                    await self.hashing.compare_password(user.password, input.password)

                with self.otel_manager.start_trace("Generate JWT Token"):
                    token = self.jwt_config.generate_token(user.user_id)

                logger.info("User logged in successfully", email=input.email)

                return ApiResponse(
                    status="success",
                    message="Login successful.",
                    data=token,
                )
            except InvalidCredentialsError as e:
                span.record_exception(e)
                logger.error("Invalid credentials", email=input.email)
                return ErrorResponse(
                    status="error",
                    message="Invalid credentials.",
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Unexpected error during login", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="Internal Server Error.",
                )