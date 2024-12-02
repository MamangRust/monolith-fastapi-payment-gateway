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
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_user_id(self, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        result = await self.session.execute(select(Saldo).filter(Saldo.user_id == id))
        saldo = result.scalars().first()
        return SaldoRecordDTO.from_orm(saldo) if saldo else None

    async def create(self, input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        new_saldo = Saldo(
            user_id=input.user_id,
            total_balance=input.total_balance,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(new_saldo)
        await self.session.commit()
        await self.session.refresh(new_saldo)
        return SaldoRecordDTO.from_orm(new_saldo)

    async def update_balance(self, input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        result = await self.session.execute(
            update(Saldo)
            .where(Saldo.user_id == input.user_id)
            .values(total_balance=input.total_balance, updated_at=datetime.utcnow())
            .returning(Saldo)
        )
        updated_saldo = result.scalars().first()
        if updated_saldo:
            await self.session.commit()
            await self.session.refresh(updated_saldo)
            return SaldoRecordDTO.from_orm(updated_saldo)
        else:
            raise ValueError("Saldo record not found")
