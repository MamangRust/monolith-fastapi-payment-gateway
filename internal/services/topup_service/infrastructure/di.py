import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from lib.config.main import get_app_settings

from lib.config.base import BaseAppSettings


from domain.repository.user import IUserRepository

from infrastructure.repository.user import UserRepository


from domain.repository.saldo import ISaldoRepository
from infrastructure.repository.saldo import SaldoRepository

from domain.repository.topup import ITopupRepository
from infrastructure.repository.topup import TopupRepository

from domain.service.topup import ITopupService
from infrastructure.service.topup import TopupService

from lib.security.jwt import JwtConfig
from lib.security.hash_password import Hashing

from lib.kafka.kafka_config import KafkaManager
from lib.otel.otel_config import OpenTelemetryManager



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
            service_name="topup-service",
            endpoint="http://jaeger:4317"
        )

    async def user_repository(self) -> IUserRepository:
        session = self._session()
        return UserRepository(session)

    async def saldo_repository(self) -> ISaldoRepository:
        session = self._session()
        return SaldoRepository(session)


    async def topup_repository(self) -> ITopupRepository:
        session = self._session()
        return TopupRepository(session)


    async def topup_service(self) -> ITopupService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()
        topup_repo = await self.topup_repository()

        return TopupService(
            user_repository=user_repo,
            saldo_repository=saldo_repo,
            topup_repository=topup_repo,
            kafka_manager=self.get_kafka(),
            otel_manager=self.get_otel()
        )


container = Container(settings=get_app_settings())



async def get_topup_service():
    return await container.topup_service()