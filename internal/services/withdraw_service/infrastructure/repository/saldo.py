from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from typing import List, Optional

from domain.dtos.request.saldo import (
    CreateSaldoRequest,
    UpdateSaldoBalanceRequest,
)
from domain.dtos.record.saldo import SaldoRecordDTO
from domain.repository.saldo import ISaldoRepository

from lib.model.saldo import Saldo
from datetime import datetime


class SaldoRepository(ISaldoRepository):
    async def find_by_user_id(self, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        result = await session.execute(select(Saldo).filter(Saldo.user_id == id))
        saldo = result.scalars().first()
        return SaldoRecordDTO.from_orm(saldo) if saldo else None

    async def create(self, input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        new_saldo = Saldo(
            user_id=input.user_id,
            balance=input.balance,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(new_saldo)
        await session.commit()
        await session.refresh(new_saldo)
        return SaldoRecordDTO.from_orm(new_saldo)

    async def update_balance(self, input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        result = await session.execute(
            update(Saldo)
            .where(Saldo.id == input.id)
            .values(balance=input.balance, updated_at=datetime.utcnow())
            .returning(Saldo)
        )
        updated_saldo = result.scalars().first()
        if updated_saldo:
            await session.commit()
            await session.refresh(updated_saldo)
            return SaldoRecordDTO.from_orm(updated_saldo)
        else:
            raise ValueError("Saldo record not found")
