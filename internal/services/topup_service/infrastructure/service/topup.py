from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from domain.repository.user import IUserRepository

from domain.repository.topup import ITopupRepository
from domain.service.topup import ITopupService

from domain.repository.saldo import ISaldoRepository

from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest, UpdateTopupAmount
from domain.dtos.request.saldo import UpdateSaldoBalanceRequest

from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.topup import TopupResponse

from lib.utils.errors import AppError, NotFoundError

from lib.kafka.kafka_config import KafkaManager
from lib.otel.otel_config import OpenTelemetryManager

import json


logger = get_logger()


class TopupService(ITopupService):
    def __init__(
        self,
        topup_repository: ITopupRepository,
        user_repository: IUserRepository,
        saldo_repository: ISaldoRepository,
        kafka_manager: KafkaManager,
        otel_manager: OpenTelemetryManager
    ):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.topup_repository = topup_repository
        self.kafka_manager = kafka_manager
        self.otel_manager = otel_manager


    

    async def get_topups(
        self,
    ) -> Union[ApiResponse[List[TopupResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get All Topups") as span:
            try:
                # Fetch all topups
                topups = await self.topup_repository.find_all()
                topup_responses = TopupResponse.from_dtos(topups)

                logger.info("Successfully retrieved topups", count=len(topup_responses))
                span.set_attribute("topup_count", len(topup_responses))

                return ApiResponse(
                    status="success",
                    message="Topups retrieved successfully",
                    data=topup_responses,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Failed to fetch topups", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )


    async def get_topup(
        self, id: int
    ) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Single Topup") as span:
            span.set_attribute("topup_id", id)

            try:
                logger.info("Fetching topup", id=id)

                # Fetch a specific topup by ID
                topup = await self.topup_repository.find_by_id(id)
                if not topup:
                    logger.error("Topup not found", id=id)
                    span.set_attribute("error", "Topup not found")
                    raise NotFoundError(f"Topup with id {id} not found")

                logger.info("Successfully retrieved topup", id=id)
                span.set_attribute("topup_found", True)

                return ApiResponse(
                    status="success",
                    message="Topup retrieved successfully",
                    data=TopupResponse.from_dto(topup),
                )
            except NotFoundError as e:
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Topup not found"
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Error fetching topup", id=id, error=str(e))
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    
    async def get_topup_users(
    self, user_id: int
    ) -> Union[ApiResponse[Optional[List[TopupResponse]]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Topups for User") as span:
            span.set_attribute("user_id", user_id)

            try:
                user = await self.user_repository.find_by_id(user_id)
                if not user:
                    logger.error(f"User with id {user_id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {user_id} not found")

                topups = await self.topup_repository.find_by_users(user_id)

                if not topups:
                    logger.info(f"No topups found for user with id {user_id}")
                    span.set_attribute("topup_count", 0)
                    return ApiResponse(
                        status="success",
                        message=f"No topups found for user with id {user_id}",
                        data=None,
                    )

                topup_response = TopupResponse.from_dtos(topups)
                logger.info(f"Successfully retrieved topups for user with id {user_id}")
                span.set_attribute("topup_count", len(topup_response))

                return ApiResponse(
                    status="success",
                    message="Success",
                    data=topup_response,
                )

            except NotFoundError as e:
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Topup or user not found"
                )

            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to fetch topups for user with id {user_id}: {e}")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )


    async def get_topup_user(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Single Topup for User") as span:
            span.set_attribute("user_id", user_id)

            try:
                user = await self.user_repository.find_by_id(user_id)
                if not user:
                    logger.error(f"User with id {user_id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {user_id} not found")

                topup = await self.topup_repository.find_by_user(user_id)

                if not topup:
                    logger.info(f"No topup found for user with id {user_id}")
                    span.set_attribute("error", "Topup not found")
                    raise NotFoundError(f"Topup with user id {user_id} not found")

                topup_response = TopupResponse.from_dto(topup)
                logger.info(f"Successfully retrieved topup for user with id {user_id}")
                span.set_attribute("topup_found", True)

                return ApiResponse(
                    status="success",
                    message="Success",
                    data=topup_response,
                )

            except NotFoundError as e:
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="Topup or user not found"
                )

            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to fetch topup for user with id {user_id}: {e}")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later."
                )

    
    async def create_topup(self, input: CreateTopupRequest) -> Union[ApiResponse[TopupResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Create Topup") as span:
            span.set_attribute("user_id", input.user_id)
            producer = None
            try:
                # Check if the user exists
                user = await self.user_repository.find_by_id(input.user_id)
                if not user:
                    logger.error(f"User with id {input.user_id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {input.user_id} not found")

                logger.info(f"User with id {input.user_id} found, proceeding with topup creation")
                span.set_attribute("user_found", True)

                # Create topup entry
                try:
                    topup = await self.topup_repository.create(input)
                    logger.info(f"Topup created for user {input.user_id}: topup amount {topup.topup_amount}")
                    span.set_attribute("topup_amount", topup.topup_amount)
                except Exception as e:
                    span.record_exception(e)
                    logger.error(f"Error creating topup for user {input.user_id}: {e}")
                    return ErrorResponse(
                        status="error",
                        message="Failed to create topup"
                    )

                # Update or create saldo
                saldo = await self.saldo_repository.find_by_user_id(input.user_id)
                try:
                    if saldo:
                        new_balance = saldo.total_balance + topup.topup_amount
                        update_request = UpdateSaldoBalanceRequest(user_id=input.user_id, total_balance=new_balance)
                        await self.saldo_repository.update_balance(update_request)
                        logger.info(f"Saldo updated successfully for user {input.user_id}. New balance: {new_balance}")
                        span.set_attribute("new_balance", new_balance)
                    else:
                        create_saldo_request = CreateSaldoRequest(user_id=input.user_id, total_balance=topup.topup_amount)
                        await self.saldo_repository.create(create_saldo_request)
                        logger.info(f"Initial saldo created for user {input.user_id} with balance {topup.topup_amount}")
                        span.set_attribute("initial_balance", topup.topup_amount)
                except Exception as db_err:
                    span.record_exception(db_err)
                    logger.error(f"Failed to update/create saldo for user {input.user_id}: {db_err}")
                    await self.topup_repository.delete(topup.topup_id)
                    return ErrorResponse(
                        status="error",
                        message=f"Failed to update/create saldo for user {input.user_id}"
                    )

                # Send email notification via Kafka
                try:
                    producer = await self.kafka_manager.get_producer()
                    email_message = {
                        "email": user.email,
                        "subject": "Top-Up Successful",
                        "body": f"Hi {user.firstname} {user.lastname}, your top-up of {topup.topup_amount} has been successfully added. Your new balance is {new_balance if saldo else topup.topup_amount}."
                    }
                    await producer.send(
                        topic="email-service-topic-topup",
                        value=json.dumps(email_message).encode("utf-8")
                    )
                    
                    logger.info(f"Email notification sent to Kafka for user {input.user_id} on topic 'email-service-topic-topup'.")
                    span.set_attribute("email_notification_sent", True)
                except Exception as kafka_err:
                    span.record_exception(kafka_err)
                    logger.error(f"Failed to send email notification for user {input.user_id}: {kafka_err}")
                    return ErrorResponse(
                        status="error",
                        message="Failed to send email notification"
                    )

                logger.info(f"Topup successfully created for user {input.user_id}. Total balance updated.")
                return ApiResponse(
                    status="success",
                    message="Topup created successfully",
                    data=TopupResponse.from_dto(topup),
                )

            except NotFoundError as e:
                span.record_exception(e)
                return ErrorResponse(
                    status="error",
                    message="An error occurred while creating topup. Please try again later."
                )

            except Exception as e:
                span.record_exception(e)
                logger.error(f"Error processing topup for user {input.user_id}: {e}")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred while creating topup"
                )
            finally:
                if producer:
                    await producer.stop()



    async def update_topup(self, input: UpdateTopupRequest) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Update Topup") as span:
            span.set_attribute("user_id", input.user_id)
            span.set_attribute("topup_id", input.topup_id)

            try:
                logger.info("Input validation passed", user_id=input.user_id, topup_id=input.topup_id)

                # Verify user existence
                user = await self.user_repository.find_by_id(input.user_id)
                if not user:
                    logger.error("User not found", user_id=input.user_id)
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {input.user_id} not found")

                logger.info("User found", user_id=input.user_id)

                # Verify topup existence
                existing_topup = await self.topup_repository.find_by_id(input.topup_id)
                if not existing_topup:
                    logger.error("Topup not found", topup_id=input.topup_id)
                    span.set_attribute("error", "Topup not found")
                    raise NotFoundError(f"Topup with id {input.topup_id} not found")

                logger.info("Topup found", topup_id=input.topup_id)

                # Calculate topup difference
                topup_difference = input.topup_amount - existing_topup.topup_amount
                logger.info(
                    "Calculating topup difference",
                    topup_difference=topup_difference,
                    new_amount=input.topup_amount,
                    old_amount=existing_topup.topup_amount,
                )
                span.set_attribute("topup_difference", topup_difference)

                # Update topup amount
                await self.topup_repository.update_amount(input=UpdateTopupAmount(topup_id=input.topup_id, topup_amount=input.topup_amount))

                # Update saldo
                saldo = await self.saldo_repository.find_by_user_id(input.user_id)
                if not saldo:
                    logger.error("Saldo not found", user_id=input.user_id)
                    span.set_attribute("error", "Saldo not found")
                    raise NotFoundError(f"Saldo for user {input.user_id} not found")

                new_balance = saldo.total_balance + topup_difference
                saldo_input = UpdateSaldoBalanceRequest(user_id=input.user_id, total_balance=new_balance)

                await self.saldo_repository.update_balance(saldo_input)

                logger.info("Saldo updated", user_id=input.user_id, new_balance=new_balance)
                span.set_attribute("new_balance", new_balance)

                # Retrieve updated topup
                updated_topup = await self.topup_repository.find_by_id(input.topup_id)
                if not updated_topup:
                    logger.error("Updated topup not found", topup_id=input.topup_id)
                    span.set_attribute("error", "Updated topup not found")
                    raise NotFoundError(f"Updated topup with id {input.topup_id} not found")

                return ApiResponse(
                    status="success",
                    message="Topup updated successfully",
                    data=TopupResponse.from_dto(updated_topup),
                )

            except AppError as e:
                span.record_exception(e)
                logger.error("Error during topup update", error=str(e))
                return ErrorResponse(
                    status="error",
                    message="Error during topup update"
                )

            except Exception as e:
                span.record_exception(e)
                logger.exception("Unexpected error during topup update")
                return ErrorResponse(
                    status="error",
                    message="Unexpected error during topup update"
                )

    async def delete_topup(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        with self.otel_manager.start_trace("Delete Topup") as span:
            span.set_attribute("topup_id", id)

            try:
                # Find user by ID
                user = await self.user_repository.find_by_id(id)
                if not user:
                    logger.error(f"User with id {id} not found")
                    span.set_attribute("error", "User not found")
                    return ErrorResponse(
                        status="error",
                        message=f"User with id {id} not found"
                    )

                # Find topup by user ID
                existing_topup = await self.topup_repository.find_by_user(user.user_id)
                if not existing_topup:
                    logger.error(f"Topup with id {id} not found")
                    span.set_attribute("error", "Topup not found")
                    return ErrorResponse(
                        status="error",
                        message=f"Topup with id {id} not found"
                    )

                # Delete topup
                await self.topup_repository.delete(existing_topup.topup_id)
                logger.info(f"Topup deleted successfully for id: {id}")

                return ApiResponse[None](
                    status="success",
                    message="Topup deleted successfully",
                    data=None,
                )

            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to delete topup for id {id}: {str(e)}")
                return ErrorResponse(
                    status="error",
                    message=f"Failed to delete topup for id {id}"
                )
