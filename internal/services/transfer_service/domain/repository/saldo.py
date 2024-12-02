import abc
from typing import List, Optional, Any
from domain.dtos.record.saldo import SaldoRecordDTO
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoBalanceRequest


class ISaldoRepository(abc.ABC):
    """
    Saldo Repository interface defining operations for saldo management.
    """

    @abc.abstractmethod
    async def find_by_user_id(self, id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update_balance(self, input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        pass
