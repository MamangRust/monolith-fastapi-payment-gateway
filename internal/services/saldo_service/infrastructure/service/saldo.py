from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger
from domain.repository.user import IUserRepository
from domain.repository.saldo import ISaldoRepository
from domain.service.saldo import ISaldoService
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse

from lib.utils.errors import AppError, NotFoundError

from domain.dtos.response.saldo import SaldoResponse
from lib.kafka.kafka_config import KafkaManager
from lib.otel.otel_config import OpenTelemetryManager

import json


logger = get_logger()


class SaldoService(ISaldoService):
    def __init__(self, user_repository: IUserRepository, saldo_repository: ISaldoRepository, kafka_manager: KafkaManager, otel_manager: OpenTelemetryManager):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.kafka_manager = kafka_manager
        self.otel_manager = otel_manager

    async def get_saldos(self) -> Union[ApiResponse[List[SaldoResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get All Saldos") as span:
            try:
                saldo = await self.saldo_repository.find_all()
                saldo_response = [SaldoResponse.from_dtos(s) for s in saldo]
                span.set_attribute("saldo_count", len(saldo_response))
                return ApiResponse(
                    status="success",
                    message="Saldos retrieved successfully",
                    data=saldo_response,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Error retrieving saldos")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    async def get_saldo(self, id: int) -> Union[ApiResponse[Optional[SaldoResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Saldo by ID") as span:
            span.set_attribute("saldo_id", id)
            try:
                saldo = await self.saldo_repository.find_by_id(id)
                if saldo:
                    return ApiResponse(
                        status="success",
                        message="Saldo retrieved successfully",
                        data=SaldoResponse.from_dto(saldo),
                    )
                else:
                    raise NotFoundError(f"Saldo with id {id} not found")
            except AppError as e:
                span.record_exception(e)
                logger.error("Error retrieving saldo", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="The requested saldo was not found."
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Error retrieving saldo")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    async def get_saldo_users(self, id: int) -> Union[ApiResponse[Optional[List[SaldoResponse]]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Saldos for User") as span:
            span.set_attribute("user_id", id)
            try:
                user = await self.user_repository.find_by_id(id)
                if not user:
                    span.set_attribute("error", "User not found")
                    raise AppError.not_found(f"User with id {id} not found")
                
                saldo = await self.saldo_repository.find_by_user_id(id)
                saldo_responses = [SaldoResponse.from_dtos(s) for s in saldo] if saldo else None

                span.set_attribute("saldo_count", len(saldo_responses) if saldo_responses else 0)
                return ApiResponse(
                    status="success",
                    message=f"No saldo found for user with id {id}" if not saldo else "Success",
                    data=saldo_responses,
                )
            except AppError as e:
                span.record_exception(e)
                logger.error("Error retrieving saldo for user", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="The requested user or saldo was not found."
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Error retrieving saldo for user")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    async def get_saldo_user(self, id: int) -> Union[ApiResponse[Optional[SaldoResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Saldo for User by ID") as span:
            span.set_attribute("user_id", id)
            try:
                user = await self.user_repository.find_by_id(id)
                if not user:
                    logger.error(f"User with id {id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {id} not found")
            except Exception as e:
                span.record_exception(e)
                logger.error(f"Error finding user with id {id}: {e}")
                return ErrorResponse(
                    status="error",
                    message=f"Error finding user with id {id}: {e}"
                )

            try:
                saldo_data = await self.saldo_repository.find_by_user_id(id)
                saldo = (
                    SaldoResponse.from_model(saldo_data)
                    if saldo_data is not None
                    else None
                )
                span.set_attribute("saldo_found", saldo is not None)
            except Exception as e:
                span.record_exception(e)
                logger.error(f"Error retrieving saldo for user with id {id}: {e}")
                return ErrorResponse(
                    status="error",
                    message=f"Error retrieving saldo for user with id {id}: {e}"
                )

            # Prepare and return the response
            if saldo is None:
                logger.info(f"No saldo found for user with id {id}")
                return ApiResponse(
                    status="success",
                    message=f"No saldo found for user with id {id}",
                    data=None,
                )

            logger.info(f"Saldo retrieved successfully for user with id {id}")
            return ApiResponse(
                status="success",
                message="Saldo retrieved successfully",
                data=saldo,
            )


    async def create_saldo(self, input: CreateSaldoRequest) -> Union[ApiResponse[SaldoResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Create Saldo") as span:
            span.set_attribute("user_id", input.user_id)
            span.set_attribute("total_balance", input.total_balance)
            try:
                user = await self.user_repository.find_by_id(input.user_id)
                if not user:
                    raise AppError.not_found(f"User with id {input.user_id} not found")

                saldo = await self.saldo_repository.create(input)
                producer = await self.kafka_manager.get_producer()
                email_message = {
                    "email": user.email,
                    "subject": "Saldo Created",
                    "body": f"Hi {user.firstname} {user.lastname}, your saldo has been successfully created with an amount of {input.total_balance}."
                }
                await producer.send_and_wait(
                    topic="email-service-topic-saldo",
                    value=json.dumps(email_message).encode("utf-8")
                )
                await producer.stop()

                logger.info("Saldo created successfully", user_id=input.user_id)
                return ApiResponse(
                    status="success",
                    message="Saldo created successfully",
                    data=SaldoResponse.from_dto(saldo),
                )
            except AppError as e:
                span.record_exception(e)
                logger.error("Error creating saldo", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An error occurred while creating saldo. Please try again later."
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Unexpected error", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    async def update_saldo(self, input: UpdateSaldoRequest) -> Union[ApiResponse[Optional[SaldoResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Update Saldo") as span:
            span.set_attribute("saldo_id", input.saldo_id)
            span.set_attribute("user_id", input.user_id)
            try:
                user = await self.user_repository.find_by_id(input.user_id)
                if not user:
                    raise NotFoundError(f"User with id {input.user_id} not found")

                existing_saldo = await self.saldo_repository.find_by_id(input.saldo_id)
                if not existing_saldo:
                    raise NotFoundError(f"Saldo with id {input.saldo_id} not found")

                updated_saldo = await self.saldo_repository.update(input)
                logger.info("Saldo updated successfully", saldo_id=input.saldo_id)
                return ApiResponse(
                    status="success",
                    message="Saldo updated successfully",
                    data=SaldoResponse.from_dto(updated_saldo),
                )
            except AppError as e:
                span.record_exception(e)
                logger.error("Error updating saldo", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An error occurred while updating saldo. Please try again later."
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Error updating saldo")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    async def delete_saldo(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        with self.otel_manager.start_trace("Delete Saldo") as span:
            span.set_attribute("user_id", id)
            try:
                # Check if the user exists
                user = await self.user_repository.find_by_id(id)
                if not user:
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {id} not found")

                # Check if the saldo exists for the user
                existing_saldo = await self.saldo_repository.find_by_user_id(user.user_id)
                if not existing_saldo:
                    span.set_attribute("error", "Saldo not found")
                    raise NotFoundError(f"Saldo with id {id} not found")

                # Proceed to delete the saldo
                await self.saldo_repository.delete(existing_saldo.saldo_id)
                span.set_attribute("saldo_deleted", True)
                return ApiResponse(
                    status="success",
                    message="Saldo deleted successfully",
                    data=None,
                )
            except AppError as e:
                span.record_exception(e)
                logger.error("Error deleting saldo", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An error occurred while deleting saldo. Please try again later."
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Unexpected error deleting saldo")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

