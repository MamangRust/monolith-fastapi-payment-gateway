import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from internal.lib.config.main import get_app_settings

from internal.lib.config.base import BaseAppSettings

from internal.services.auth_service.domain.repository.user import IUserRepository

from internal.services.auth_service.infrastructure.repository.user import UserRepository


from internal.services.auth_service.domain.service.auth import IAuthService

from internal.services.auth_service.infrastructure.service.auth import AuthService

from internal.lib.security.jwt import JwtConfig
from internal.lib.security.hash_password import Hashing
from internal.lib.otel.otel_config import OpenTelemetryManager

class Container:
    def __init__(self, settings: BaseAppSettings) -> None:
        self._settings = settings
        self._engine = create_async_engine(**settings.sqlalchemy_engine_props)
        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)


    def get_jwt(self) -> JwtConfig:
        return JwtConfig(self._settings.jwt_secret_key, self._settings.jwt_token_expiration_minutes)

    def get_otel(self) -> OpenTelemetryManager:
        return OpenTelemetryManager(
            service_name="auth-service",
            endpoint="http://jaeger:4317"
        )

    async def user_repository(self) -> IUserRepository:
        session = self._session()
        return UserRepository(session)

    async def auth_service(self) -> IAuthService:
        user_repo = await self.user_repository()
        return AuthService(
            repository=user_repo,
            hashing=Hashing(),
            jwt_config=self.get_jwt(),
            otel_manager=self.get_otel()
        )

container = Container(settings=get_app_settings())



async def get_auth_service():
    return await container.auth_service()