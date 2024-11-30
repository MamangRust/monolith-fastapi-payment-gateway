import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from internal.lib.config.main import get_app_settings

from internal.lib.config.base import BaseAppSettings


from internal.services.withdraw_service.domain.repository.user import IUserRepository
from internal.services.withdraw_service.infrastructure.repository.user import UserRepository


from internal.services.withdraw_service.domain.repository.saldo import ISaldoRepository
from internal.services.withdraw_service.infrastructure.repository.saldo import SaldoRepository

from internal.services.withdraw_service.domain.repository.withdraw import IWithdrawRepository
from internal.services.withdraw_service.infrastructure.repository.withdraw import WithdrawRepository

from internal.services.withdraw_service.domain.service.withdraw import IWithdrawService
from internal.services.withdraw_service.infrastructure.service.withdraw import WithdrawService

from internal.lib.security.jwt import JwtConfig
from internal.lib.security.hash_password import Hashing

from internal.lib.kafka.kafka_config import KafkaManager
from internal.lib.otel.otel_config import OpenTelemetryManager


class Container:
    def __init__(self, settings: BaseAppSettings) -> None:
        self._settings = settings
        self._engine = create_async_engine(**settings.sqlalchemy_engine_props)
        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)


    def get_jwt(self) -> JwtConfig:
        return JwtConfig(self._settings.jwt_secret_key, self._settings.jwt_token_expiration_minutes)

    def get_kafka(self) -> KafkaManager:
        return KafkaManager(
            bootstrap_servers="kafka:9092"
        )

    def get_otel(self) -> OpenTelemetryManager:
        return OpenTelemetryManager(
            service_name="withdraw-service",
            endpoint="http://jaeger:4317"
        )


    async def user_repository(self) -> IUserRepository:
        session = self._session()
        return UserRepository(session)

    async def saldo_repository(self) -> ISaldoRepository:
        session = self._session()
        return SaldoRepository(session)


    async def withdraw_repository(self) -> IWithdrawRepository:
        session = self._session()
        return WithdrawRepository(session)

    async def withdraw_service(self) -> IWithdrawService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()
        withdraw_repo = await self.withdraw_repository()

        return WithdrawService(
            user_repository=user_repo,
            saldo_repository=saldo_repo,
            withdraw_repository=withdraw_repo,
            kafka_manager=self.get_kafka(),
            otel_manager=self.get_otel()
        )

container = Container(settings=get_app_settings())



async def get_withdraw_service():
    return await container.withdraw_service()