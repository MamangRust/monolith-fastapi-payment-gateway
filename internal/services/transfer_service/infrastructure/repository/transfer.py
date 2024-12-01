from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime
from typing import List, Optional

from domain.dtos.request.transfer import (
    CreateTransferRequest,
    UpdateTransferRequest,
    UpdateTransferAmountRequest,
)
from domain.dtos.record.transfer import (
    TransferRecordDTO,
)
from domain.repository.transfer import (
    ITransferRepository,
)
from lib.model.transfer import Transfer


class TransferRepository(ITransferRepository):
    async def find_all(self) -> List[TransferRecordDTO]:
        """
        Retrieve all transfer records.
        """
        result = await session.execute(select(Transfer))
        transfers = result.scalars().all()
        return [TransferRecordDTO.from_orm(transfer) for transfer in transfers]

    async def find_by_id(self, id: int) -> Optional[TransferRecordDTO]:
        """
        Find a transfer record by its ID.
        """
        result = await session.execute(select(Transfer).filter(Transfer.id == id))
        transfer = result.scalars().first()
        return TransferRecordDTO.from_orm(transfer) if transfer else None

    async def find_by_users(self, user_id: int) -> Optional[List[TransferRecordDTO]]:
        """
        Find all transfer records associated with a given user ID.
        """
        result = await session.execute(
            select(Transfer).filter(Transfer.user_id == user_id)
        )
        transfers = result.scalars().all()
        return (
            [TransferRecordDTO.from_orm(transfer) for transfer in transfers]
            if transfers
            else None
        )

    async def find_by_user(self, user_id: int) -> Optional[TransferRecordDTO]:
        """
        Find a single transfer record associated with a given user ID.
        """
        result = await session.execute(
            select(Transfer).filter(Transfer.user_id == user_id)
        )
        transfer = result.scalars().first()
        return TransferRecordDTO.from_orm(transfer) if transfer else None

    async def create(self, input: CreateTransferRequest) -> TransferRecordDTO:
        """
        Create a new transfer record from the given input.
        """
        new_transfer = Transfer(
            user_id=input.user_id,
            amount=input.amount,
            recipient_id=input.recipient_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(new_transfer)
        await session.commit()
        await session.refresh(new_transfer)
        return TransferRecordDTO.from_orm(new_transfer)

    async def update(self, input: UpdateTransferRequest) -> TransferRecordDTO:
        """
        Update an existing transfer record based on the given input.
        """
        result = await session.execute(
            update(Transfer)
            .where(Transfer.id == input.id)
            .values(
                user_id=input.user_id,
                amount=input.amount,
                recipient_id=input.recipient_id,
                updated_at=datetime.utcnow(),
            )
            .returning(Transfer)
        )
        updated_transfer = result.scalars().first()
        if updated_transfer:
            await session.commit()
            await session.refresh(updated_transfer)
            return TransferRecordDTO.from_orm(updated_transfer)
        else:
            raise ValueError("Transfer record not found")

    async def update_amount(
        self, input: UpdateTransferAmountRequest
    ) -> TransferRecordDTO:
        """
        Update the amount of an existing transfer record.
        """
        result = await session.execute(
            update(Transfer)
            .where(Transfer.id == input.id)
            .values(amount=input.amount, updated_at=datetime.utcnow())
            .returning(Transfer)
        )
        updated_transfer = result.scalars().first()
        if updated_transfer:
            await session.commit()
            await session.refresh(updated_transfer)
            return TransferRecordDTO.from_orm(updated_transfer)
        else:
            raise ValueError("Transfer record not found")

    async def delete(self, id: int) -> None:
        """
        Delete a transfer record by its ID.
        """
        result = await session.execute(delete(Transfer).where(Transfer.id == id))
        if result.rowcount == 0:
            raise ValueError("Transfer record not found")
        await session.commit()
