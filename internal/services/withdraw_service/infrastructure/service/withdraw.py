from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from domain.repository.user import IUserRepository

from domain.repository.withdraw import (
    IWithdrawRepository,
)
from domain.service.withdraw import IWithdrawService

from domain.repository.saldo import ISaldoRepository


from domain.dtos.request.withdraw import (
    CreateWithdrawRequest,
    UpdateWithdrawRequest,
)

from domain.dtos.response.api import (
    ApiResponse,
    ErrorResponse,
)
from lib.utils.errors import AppError, NotFoundError, ValidationError

from domain.dtos.response.withdraw import (
    WithdrawResponse,
)

from lib.kafka.kafka_config import KafkaManager
from lib.otel.otel_config import OpenTelemetryManager


logger = get_logger()


class WithdrawService(IWithdrawService):
    def __init__(
        self,
        withdraw_repository: IWithdrawRepository,
        user_repository: IUserRepository,
        saldo_repository: ISaldoRepository,
        kafka_manager: KafkaManager,
        otel_manager: OpenTelemetryManager,
    ):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.withdraw_repository = withdraw_repository
        self.kafka_manager = kafka_manager
        self.otel_manager = otel_manager

    async def get_withdraws(
        self,
    ) -> Union[ApiResponse[List[WithdrawResponse]], ErrorResponse]:
        """
        Retrieve all withdrawal records.
        """
        with self.otel_manager.start_trace("Get Withdraws") as span:
            try:
                withdraws = await self.withdraw_repository.find_all()
                withdraw_responses = [WithdrawResponse.from_dtos(w) for w in withdraws]

                span.set_attribute("total_withdrawals", len(withdraw_responses))
                logger.info(f"Successfully fetched {len(withdraw_responses)} withdrawals.")
                return ApiResponse(
                    status="success",
                    message="Withdrawals retrieved successfully.",
                    data=withdraw_responses,
                )
            except Exception as e:
                logger.error(f"Failed to fetch withdrawals: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later.",
                )

    async def get_withdraw(
        self, id: int
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Withdrawal by ID") as span:
            span.set_attribute("withdraw_id", id)
            try:
                withdraw = await self.withdraw_repository.find_by_id(id)

                if withdraw:
                    span.set_attribute("withdraw_found", True)
                    logger.info(f"Successfully retrieved withdrawal with ID: {id}.")
                    return ApiResponse(
                        status="success",
                        message="Withdrawal retrieved successfully.",
                        data=WithdrawResponse.from_dto(withdraw),
                    )
                else:
                    span.set_attribute("withdraw_found", False)
                    logger.error(f"Withdrawal with ID {id} not found.")
                    raise NotFoundError(f"Withdrawal with ID {id} not found.")
            except Exception as e:
                logger.error(f"Failed to retrieve withdrawal with ID {id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later.",
                )

    async def get_withdraw_users(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[List[WithdrawResponse]]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Withdraws by User ID") as span:
            span.set_attribute("user_id", user_id)
            try:
                user = await self.user_repository.find_by_id(user_id)
                if not user:
                    logger.error(f"User with ID {user_id} not found.")
                    span.set_attribute("user_found", False)
                    return NotFoundError(f"User with ID {user_id} not found.")

                # Retrieve withdrawals for the user
                withdrawals = await self.withdraw_repository.find_by_users(user_id)
                if not withdrawals:
                    logger.info(f"No withdrawals found for user with ID {user_id}.")
                    span.set_attribute("withdrawals_found", False)
                    return ApiResponse(
                        status="success",
                        message=f"No withdrawals found for user with ID {user_id}.",
                        data=None,
                    )

                # Map withdrawals to response DTOs
                withdrawal_responses = [WithdrawResponse.from_dtos(w) for w in withdrawals]

                logger.info(f"Successfully retrieved withdrawals for user with ID {user_id}.")
                span.set_attribute("withdrawals_found", True)
                span.set_attribute("total_withdrawals", len(withdrawals))

                return ApiResponse(
                    status="success",
                    message="Withdrawals retrieved successfully.",
                    data=withdrawal_responses,
                )
            except Exception as e:
                logger.error(f"Failed to retrieve withdrawals for user with ID {user_id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error",
                    message="An unexpected error occurred. Please try again later.",
                )

    async def get_withdraw_user(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Withdrawal by User ID") as span:
            span.set_attribute("user_id", user_id)
            try:
                # Check if the user exists
                user = await self.user_repository.find_by_id(user_id)
                if not user:
                    logger.error(f"User with ID {user_id} not found.")
                    span.set_attribute("user_found", False)
                    raise NotFoundError(f"User with ID {user_id} not found.")

                # Retrieve the withdrawal for the user
                withdrawal = await self.withdraw_repository.find_by_user(user_id)
                if not withdrawal:
                    logger.info(f"No withdrawal found for user with ID {user_id}.")
                    span.set_attribute("withdrawal_found", False)
                    raise NotFoundError(f"Withdrawal for user with ID {user_id} not found.")

                # Map withdrawal to response DTO
                withdrawal_response = WithdrawResponse.from_dto(withdrawal)
                logger.info(f"Successfully retrieved withdrawal for user with ID {user_id}.")
                span.set_attribute("withdrawal_found", True)

                return ApiResponse(
                    status="success",
                    message="Withdrawal retrieved successfully.",
                    data=withdrawal_response,
                )
            except Exception as e:
                logger.error(f"Failed to retrieve withdrawal for user with ID {user_id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error",
                    message=f"Failed to retrieve withdrawal for user with ID {user_id}",
                )

    async def create_withdraw(
        self, input: CreateWithdrawRequest
    ) -> Union[ApiResponse[WithdrawResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Create Withdraw") as span:
            span.set_attribute("user_id", input.user_id)
            try:
                logger.info(f"Creating withdraw for user_id: {input.user_id}")

                # Check if the saldo exists for the user
                saldo = await self.saldo_repository.find_by_user_id(input.user_id)
                if not saldo:
                    logger.error(f"Saldo with user_id {input.user_id} not found")
                    span.set_attribute("saldo_found", False)
                    raise NotFoundError(f"Saldo with user_id {input.user_id} not found")

                # Check if the user has sufficient balance
                if saldo.total_balance < input.withdraw_amount:
                    logger.error(
                        f"Insufficient balance for user_id {input.user_id}. "
                        f"Attempted withdrawal: {input.withdraw_amount}"
                    )
                    span.set_attribute("sufficient_balance", False)
                    raise ValidationError("Insufficient balance")

                logger.info("User has sufficient balance for withdrawal")
                span.set_attribute("sufficient_balance", True)

                # Deduct the withdraw amount from the user's balance
                new_total_balance = saldo.total_balance - input.withdraw_amount
                try:
                    await self.saldo_repository.update_saldo_withdraw(
                        user_id=input.user_id,
                        withdraw_amount=input.withdraw_amount,
                        withdraw_time=datetime.utcnow(),
                        total_balance=new_total_balance,
                    )
                    logger.info(
                        f"Saldo balance updated for user_id {input.user_id}. "
                        f"New balance: {new_total_balance}"
                    )
                except Exception as e:
                    logger.error(f"Failed to update saldo balance: {e}")
                    span.record_exception(e)
                    span.set_attribute("error", "Failed to update saldo balance")
                    return ErrorResponse(
                        status="error", message=f"Failed to update saldo balance: {e}"
                    )

                # Create the withdraw record
                try:
                    withdraw_record = await self.withdraw_repository.create(input)
                    logger.info(f"Withdraw created successfully for user_id {input.user_id}")
                    span.set_attribute("withdraw_created", True)

                    # Kirim pesan Kafka untuk memberi tahu layanan lain bahwa penarikan telah dibuat
                    message = {
                        "user_id": input.user_id,
                        "withdraw_amount": input.withdraw_amount,
                        "new_total_balance": new_total_balance,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    # Menggunakan self.kafka_manager untuk mengirim pesan
                    await self.kafka_manager.produce_message(
                        topic="withdraw-topic",
                        key=str(input.user_id),
                        value=message
                    )
                    logger.info(f"Message sent to Kafka topic 'withdraw-topic' for user_id {input.user_id}")

                    return ApiResponse(
                        status="success",
                        message="Withdraw created successfully",
                        data=WithdrawResponse.from_dto(withdraw_record),
                    )
                except Exception as e:
                    logger.error(f"Failed to create withdraw: {e}")
                    span.record_exception(e)
                    span.set_attribute("error", "Failed to create withdraw")
                    return ErrorResponse(
                        status="error", message=f"Failed to create withdraw: {e}"
                    )
            except Exception as e:
                logger.error(f"Unexpected error while creating withdraw for user_id {input.user_id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error", message="An unexpected error occurred. Please try again later."
                )


    async def update_withdraw(
        self, input: UpdateWithdrawRequest
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Update Withdraw") as span:
            span.set_attribute("withdraw_id", input.withdraw_id)
            span.set_attribute("user_id", input.user_id)
            try:
                # Check if the withdrawal exists
                withdraw_record = await self.withdraw_repository.find_by_id(input.withdraw_id)
                if not withdraw_record:
                    logger.error(f"Withdraw with id {input.withdraw_id} not found")
                    span.set_attribute("withdraw_found", False)
                    raise NotFoundError(f"Withdraw with id {input.withdraw_id} not found")

                # Fetch the user's saldo
                saldo = await self.saldo_repository.find_by_user_id(input.user_id)
                if not saldo:
                    logger.error(f"Saldo with user_id {input.user_id} not found")
                    span.set_attribute("saldo_found", False)
                    raise NotFoundError(f"Saldo with user_id {input.user_id} not found")

                # Check if the new withdrawal amount can be updated within the current balance
                new_total_balance = saldo.total_balance - input.withdraw_amount
                if new_total_balance < 0:
                    logger.error(
                        f"Insufficient balance for user_id {input.user_id}. "
                        f"Attempted withdrawal: {input.withdraw_amount}"
                    )
                    span.set_attribute("sufficient_balance", False)
                    raise ValidationError("Insufficient balance")

                span.set_attribute("sufficient_balance", True)

                # Try updating the withdrawal record
                try:
                    updated_withdraw = await self.withdraw_repository.update(input)
                except Exception as e:
                    # Rollback saldo if the withdrawal update fails
                    await self.saldo_repository.update_saldo_withdraw(
                        user_id=input.user_id,
                        withdraw_amount=None,
                        withdraw_time=None,
                        total_balance=saldo.total_balance,
                    )
                    logger.error(
                        f"Rollback: Saldo reverted due to withdraw update failure: {e}"
                    )
                    span.record_exception(e)
                    return ErrorResponse(
                        status="error",
                        message=f"Rollback: Saldo reverted due to withdraw update failure",
                    )

                # Update the saldo to reflect the new withdrawal amount
                try:
                    await self.saldo_repository.update_saldo_withdraw(
                        user_id=input.user_id,
                        withdraw_amount=input.withdraw_amount,
                        withdraw_time=datetime.utcnow(),
                        total_balance=new_total_balance,
                    )
                except Exception as e:
                    logger.error(f"Failed to update saldo balance after withdrawal update: {e}")
                    span.record_exception(e)
                    return ErrorResponse(
                        status="error",
                        message=f"Failed to update saldo balance after withdrawal update",
                    )

                logger.info(
                    f"Withdraw updated successfully for withdraw_id {input.withdraw_id}"
                )
                span.set_attribute("withdraw_updated", True)

                return ApiResponse(
                    status="success",
                    message="Withdraw updated successfully",
                    data=WithdrawResponse.from_dto(updated_withdraw),
                )
            except Exception as e:
                logger.error(f"Unexpected error while updating withdraw for withdraw_id {input.withdraw_id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred.")
                return ErrorResponse(
                    status="error",
                    message=f"Failed to update withdraw for withdraw_id {input.withdraw_id}",
                )

    async def delete_withdraw(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        with self.otel_manager.start_trace("Delete Withdraw") as span:
            span.set_attribute("withdraw_id", id)
            try:
                # Check if the withdraw exists
                existing_withdraw = await self.withdraw_repository.find_by_id(id)
                if not existing_withdraw:
                    logger.error(f"Withdraw with id {id} not found")
                    span.set_attribute("withdraw_found", False)
                    raise NotFoundError(f"Withdraw with id {id} not found")

                # Attempt to delete the withdraw record
                try:
                    await self.withdraw_repository.delete(id)
                    logger.info(f"Withdraw deleted successfully for id: {id}")
                    span.set_attribute("withdraw_deleted", True)
                except Exception as e:
                    logger.error(f"Error deleting withdraw with id {id}: {e}")
                    span.record_exception(e)
                    span.set_attribute("error", "Error occurred while deleting withdraw")
                    return ErrorResponse(
                        status="error", message=f"Error deleting withdraw with id {id}"
                    )

                # Return a success response
                logger.info(f"Withdraw with id {id} deleted successfully")
                return ApiResponse(
                    status="success",
                    message="Withdraw deleted successfully",
                    data=None,
                )
            except Exception as e:
                logger.error(f"Unexpected error while deleting withdraw with id {id}: {str(e)}")
                span.record_exception(e)
                span.set_attribute("error", "An unexpected error occurred")
                return ErrorResponse(
                    status="error",
                    message=f"Failed to delete withdraw with id {id}"
                )
