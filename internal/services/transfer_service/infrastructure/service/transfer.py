import json
from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger


from domain.repository.user import IUserRepository

from domain.repository.transfer import (
    ITransferRepository,
)
from domain.service.transfer import ITransferService

from domain.repository.saldo import ISaldoRepository


from domain.dtos.request.transfer import (
    CreateTransferRequest,
    UpdateTransferRequest,
    UpdateTransferAmountRequest,
)

from domain.dtos.request.saldo import UpdateSaldoBalanceRequest

from domain.dtos.response.api import (
    ApiResponse,
    ErrorResponse,
)
from lib.utils.errors import AppError, NotFoundError, ValidationError
from domain.dtos.response.transfer import (
    TransferResponse,
)
from lib.kafka.kafka_config import KafkaManager
from lib.otel.otel_config import OpenTelemetryManager


logger = get_logger()


class TransferService(ITransferService):
    def __init__(
        self,
        transfer_repository: ITransferRepository,
        user_repository: IUserRepository,
        saldo_repository: ISaldoRepository,
        kafka_manager: KafkaManager,
        otel_manager: OpenTelemetryManager,
    ):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.transfer_repository = transfer_repository
        self.kafka_manager = kafka_manager
        self.otel_manager = otel_manager

    async def get_transfers(
        self,
    ) -> Union[ApiResponse[List[TransferResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Transfers") as span:
            try:
                logger.info("Retrieving all transfers")
                transfers = await self.transfer_repository.find_all()
                transfer_responses = TransferResponse.from_dtos(transfers)

                logger.info(f"Successfully retrieved {len(transfers)} transfers")
                span.set_attribute("transfer_count", len(transfers))

                return ApiResponse(
                    status="success",
                    message="Transfers retrieved successfully",
                    data=transfer_responses,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error("Failed to retrieve transfers", error=str(e))
                return ErrorResponse(
                    status="error", message="Failed to retrieve transfers"
                )

    async def get_transfer(
        self, id: int
    ) -> Union[ApiResponse[Optional[TransferResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Transfer") as span:
            span.set_attribute("transfer_id", id)

            try:
                logger.info(f"Retrieving transfer with id {id}")
                transfer = await self.transfer_repository.find_by_id(id)

                if transfer is None:
                    logger.error(f"Transfer with id {id} not found")
                    span.set_attribute("error", "Transfer not found")
                    raise NotFoundError(f"Transfer with id {id} not found")

                transfer_response = TransferResponse.from_dto(transfer)
                logger.info(f"Successfully retrieved transfer with id {id}")

                return ApiResponse(
                    status="success",
                    message="Transfer retrieved successfully",
                    data=transfer_response,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to retrieve transfer with id {id}", error=str(e))
                return ErrorResponse(
                    status="error", message=f"Failed to retrieve transfer with id {id}"
                )

    async def get_transfer_users(
        self, id: int
    ) -> Union[ApiResponse[Optional[List[TransferResponse]]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Transfer Users") as span:
            span.set_attribute("user_id", id)
            try:
                logger.info(f"Retrieving transfers for user with id {id}")
                user = await self.user_repository.find_by_id(id)
                if user is None:
                    logger.error(f"User with id {id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {id} not found")

                transfers = await self.transfer_repository.find_by_users(id)
                transfer_responses = TransferResponse.from_dtos(transfers)

                logger.info(
                    f"Successfully retrieved {len(transfer_responses) if transfer_responses else 0} transfers for user {id}"
                )
                span.set_attribute(
                    "transfer_count",
                    len(transfer_responses) if transfer_responses else 0,
                )

                return ApiResponse(
                    status="success",
                    message="Transfers retrieved successfully",
                    data=transfer_responses,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error(
                    f"Failed to retrieve transfers for user {id}", error=str(e)
                )
                return ErrorResponse(
                    status="error",
                    message=f"Failed to retrieve transfers for user {id}",
                )

    async def get_transfer_user(
        self, id: int
    ) -> Union[ApiResponse[Optional[TransferResponse]], ErrorResponse]:
        with self.otel_manager.start_trace("Get Transfer User") as span:
            span.set_attribute("user_id", id)
            try:
                logger.info(f"Retrieving transfer for user with id {id}")
                user = await self.user_repository.find_by_id(id)
                if user is None:
                    logger.error(f"User with id {id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {id} not found")

                transfer = await self.transfer_repository.find_by_user(id)
                transfer_response = (
                    TransferResponse.from_dto(transfer)
                    if transfer is not None
                    else None
                )

                if transfer_response is not None:
                    logger.info(
                        f"Successfully retrieved transfer for user with id {id}"
                    )
                else:
                    logger.info(f"No transfer found for user with id {id}")

                return ApiResponse(
                    status="success",
                    message="Transfer retrieved successfully",
                    data=transfer_response,
                )
            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to retrieve transfer for user {id}", error=str(e))
                return ErrorResponse(
                    status="error", message=f"Failed to retrieve transfer for user {id}"
                )

    async def create_transfer(
        self, input: CreateTransferRequest
    ) -> Union[ApiResponse[TransferResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Create Transfer") as span:
            span.set_attribute("transfer_from", input.transfer_from)
            span.set_attribute("transfer_to", input.transfer_to)
            span.set_attribute("transfer_amount", input.transfer_amount)

            producer = None

            try:
                # Check sender user
                sender = await self.user_repository.find_by_id(input.transfer_from)
                if sender is None:
                    logger.error(f"User with id {input.transfer_from} not found")
                    span.set_attribute("error", "Sender not found")
                    raise NotFoundError(f"User with id {input.transfer_from} not found")

                # Check receiver user
                receiver = await self.user_repository.find_by_id(input.transfer_to)
                if receiver is None:
                    logger.error(f"User with id {input.transfer_to} not found")
                    span.set_attribute("error", "Receiver not found")
                    raise NotFoundError(f"User with id {input.transfer_to} not found")

                # Create transfer record
                transfer = await self.transfer_repository.create(input)

                # Update sender balance
                sender_saldo = await self.saldo_repository.find_by_user_id(
                    input.transfer_from
                )
                if sender_saldo is None:
                    logger.error(f"Saldo with User id {input.transfer_from} not found")
                    span.set_attribute("error", "Sender saldo not found")
                    raise NotFoundError(
                        f"Saldo with User id {input.transfer_from} not found"
                    )

                sender_balance = sender_saldo.total_balance - input.transfer_amount
                request_sender_balance = UpdateSaldoBalanceRequest(
                    user_id=input.transfer_from,
                    total_balance=sender_balance,
                )

                # Rollback transfer if updating sender's balance fails
                try:
                    await self.saldo_repository.update_balance(request_sender_balance)
                except Exception as db_err:
                    logger.error(f"Failed to update saldo balance for sender: {db_err}")
                    span.record_exception(db_err)
                    await self.transfer_repository.delete(transfer.transfer_id)
                    return ErrorResponse(
                        status="error",
                        message="Failed to update saldo balance for sender",
                    )

                # Update receiver balance
                receiver_saldo = await self.saldo_repository.find_by_user_id(
                    input.transfer_to
                )
                if receiver_saldo is None:
                    logger.error(f"Saldo with User id {input.transfer_to} not found")
                    span.set_attribute("error", "Receiver saldo not found")
                    raise NotFoundError(
                        f"Saldo with User id {input.transfer_to} not found"
                    )

                receiver_balance = receiver_saldo.total_balance + input.transfer_amount
                request_receiver_balance = UpdateSaldoBalanceRequest(
                    user_id=input.transfer_to,
                    total_balance=receiver_balance,
                )

                # Rollback transfer if updating receiver's balance fails
                try:
                    await self.saldo_repository.update_balance(request_receiver_balance)
                except Exception as db_err:
                    logger.error(
                        f"Failed to update saldo balance for receiver: {db_err}"
                    )
                    span.record_exception(db_err)
                    await self.transfer_repository.delete(transfer.transfer_id)
                    return ErrorResponse(
                        status="error",
                        message="Failed to update saldo balance for receiver",
                    )

                # Send Kafka message for email notification
                producer = await self.kafka_manager.get_producer()
                email_message = {
                    "sender_email": sender.email,
                    "receiver_email": receiver.email,
                    "subject": "Transfer Successful",
                    "body": (
                        f"Hi {sender.firstname} {sender.lastname}, you have successfully transferred {input.transfer_amount} to {receiver.firstname} {receiver.lastname}. "
                        f"Your new balance is {sender_balance}. \n\n"
                        f"Hi {receiver.firstname} {receiver.lastname}, you have received {input.transfer_amount} from {sender.firstname} {sender.lastname}. "
                        f"Your new balance is {receiver_balance}."
                    ),
                }
                await producer.send(
                    topic="email-service-topic-transfer",
                    value=json.dumps(email_message).encode("utf-8"),
                )
                await producer.stop()
                logger.info(
                    f"Email notification sent to Kafka for transfer from {input.transfer_from} to {input.transfer_to}."
                )

                return ApiResponse(
                    status="success",
                    message="Transfer created successfully",
                    data=TransferResponse.from_dto(transfer),
                )

            except NotFoundError as e:
                span.record_exception(e)
                logger.error(f"Not found: {e}")
                return ErrorResponse(status="error", message=str(e))

            except Exception as e:
                span.record_exception(e)
                logger.error(f"Failed to create transfer: {e}")
                return ErrorResponse(
                    status="error", message="Failed to create transfer"
                )
            finally:
                if producer:
                    await producer.stop()

    async def update_transfer(
        self, input: UpdateTransferRequest
    ) -> Union[ApiResponse[TransferResponse], ErrorResponse]:
        with self.otel_manager.start_trace("Update Transfer") as span:
            span.set_attribute("transfer_id", input.transfer_id)
            span.set_attribute("new_transfer_amount", input.transfer_amount)

            try:
                # Retrieve the existing transfer
                transfer = await self.transfer_repository.find_by_id(input.transfer_id)
                if not transfer:
                    logger.error(f"Transfer with id {input.transfer_id} not found")
                    span.set_attribute("error", "Transfer not found")
                    raise NotFoundError(
                        f"Transfer with id {input.transfer_id} not found"
                    )

                # Calculate the difference in transfer amount
                amount_difference = input.transfer_amount - transfer.transfer_amount

                # Update sender's saldo
                sender_saldo = await self.saldo_repository.find_by_user_id(
                    transfer.transfer_from
                )
                if not sender_saldo:
                    logger.error(
                        f"Saldo with User id {transfer.transfer_from} not found"
                    )
                    span.set_attribute("error", "Sender saldo not found")
                    raise NotFoundError(
                        f"Saldo with User id {transfer.transfer_from} not found"
                    )

                new_sender_balance = sender_saldo.total_balance - amount_difference

                if new_sender_balance < 0:
                    logger.error("Insufficient balance for sender")
                    span.set_attribute("error", "Insufficient balance")
                    raise ValidationError("Insufficient balance for sender")

                update_sender_balance = UpdateSaldoBalanceRequest(
                    user_id=transfer.transfer_from,
                    total_balance=new_sender_balance,
                )

                # Update the sender's balance in the repository
                try:
                    await self.saldo_repository.update_balance(update_sender_balance)
                except Exception as db_err:
                    logger.error(f"Failed to update sender's saldo: {db_err}")
                    span.record_exception(db_err)
                    return ErrorResponse(
                        status="error", message=f"Failed to update sender's saldo"
                    )

                # Update receiver's saldo
                receiver_saldo = await self.saldo_repository.find_by_user_id(
                    transfer.transfer_to
                )
                if not receiver_saldo:
                    logger.error(f"Saldo with User id {transfer.transfer_to} not found")
                    span.set_attribute("error", "Receiver saldo not found")
                    raise NotFoundError(
                        f"Saldo with User id {transfer.transfer_to} not found"
                    )

                new_receiver_balance = receiver_saldo.total_balance + amount_difference

                update_receiver_balance = UpdateSaldoBalanceRequest(
                    user_id=transfer.transfer_to,
                    total_balance=new_receiver_balance,
                )

                # Update the receiver's balance in the repository
                try:
                    await self.saldo_repository.update_balance(update_receiver_balance)
                except Exception as db_err:
                    logger.error(f"Failed to update receiver's saldo: {db_err}")
                    span.record_exception(db_err)

                    # Rollback sender's saldo update if receiver's update fails
                    rollback_sender_balance = UpdateSaldoBalanceRequest(
                        user_id=transfer.transfer_from,
                        total_balance=sender_saldo.total_balance,
                    )

                    try:
                        await self.saldo_repository.update_balance(
                            rollback_sender_balance
                        )
                    except Exception as rollback_err:
                        logger.error(
                            f"Failed to rollback sender's saldo update: {rollback_err}"
                        )
                        span.record_exception(rollback_err)

                    return ErrorResponse(f"Failed to rollback sender's saldo update")

                # Update the transfer record
                updated_transfer = await self.transfer_repository.update(input)
                return ApiResponse(
                    status="success",
                    message="Transfer updated successfully",
                    data=TransferResponse.from_dto(updated_transfer),
                )

            except Exception as e:
                logger.error(f"Failed to update transfer: {e}")
                span.record_exception(e)
                return ErrorResponse(
                    status="error", message="Failed to update transfer"
                )

    async def delete_transfer(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        with self.otel_manager.start_trace("Delete Transfer") as span:
            span.set_attribute("user_id", id)

            try:
                # Retrieve the user
                user = await self.user_repository.find_by_id(id)
                if not user:
                    logger.error(f"User with id {id} not found")
                    span.set_attribute("error", "User not found")
                    raise NotFoundError(f"User with id {id} not found")

                # Retrieve the transfer associated with the user
                existing_transfer = await self.transfer_repository.find_by_user(
                    user.user_id
                )
                if existing_transfer:
                    try:
                        # Delete the transfer
                        await self.transfer_repository.delete(
                            existing_transfer.transfer_id
                        )
                        logger.info(f"Transfer deleted successfully for id: {id}")
                        span.set_attribute("transfer_id", existing_transfer.transfer_id)

                        return ApiResponse(
                            status="success",
                            message="Transfer deleted successfully",
                            data=None,
                        )
                    except Exception as db_err:
                        logger.error(
                            f"Failed to delete transfer for user id {id}: {db_err}"
                        )
                        span.record_exception(db_err)
                        span.set_attribute("error", "Failed to delete transfer")
                        return ErrorResponse(
                            status="error",
                            message=f"Failed to delete transfer for user id {id}",
                        )
                else:
                    logger.error(f"Transfer with user id {id} not found")
                    span.set_attribute("error", "Transfer not found")
                    raise NotFoundError(f"Transfer with user id {id} not found")

            except Exception as e:
                logger.error(f"Failed to delete transfer: {e}")
                span.record_exception(e)
                return ErrorResponse(
                    status="error", message="Failed to delete transfer"
                )
