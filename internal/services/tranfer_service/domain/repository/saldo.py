import abc
from typing import List, Optional, Any
from internal.services.tranfer_service.domain.dtos.record.saldo import SaldoRecordDTO
from internal.services.tranfer_service.domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoBalanceRequest


class ISaldoRepository(abc.ABC):
    """
    Saldo Repository interface defining operations for saldo management.
    """
    @abc.abstractmethod
    async def find_by_user_id(self, session: Any,id: int) -> Optional[SaldoRecordDTO]:
        """
        Find a single saldo record associated with a given user ID.
        """
        pass

    @abc.abstractmethod
    async def create(self, session: Any,input: CreateSaldoRequest) -> SaldoRecordDTO:
        """
        Create a new saldo record from the given input.
        """
        pass

    @abc.abstractmethod
    async def update_balance(self, session: Any,input: UpdateSaldoBalanceRequest) -> SaldoRecordDTO:
        """
        Update the balance of an existing saldo record.
        """
        pass