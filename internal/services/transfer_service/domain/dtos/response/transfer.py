from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.dtos.record.transfer import TransferRecordDTO

class TransferResponse(BaseModel):
    transfer_id: int
    transfer_from: int
    transfer_to: int
    transfer_amount: int
    transfer_time: datetime

    @staticmethod
    def from_dto(dto: TransferRecordDTO) -> 'TransferResponse':
        """
        Converts a TransferRecordDTO to a TransferResponse.
        """
        return TransferResponse(
            transfer_id=dto.transfer_id,
            transfer_from=dto.transfer_from,
            transfer_to=dto.transfer_to,
            transfer_amount=dto.transfer_amount,
            transfer_time=dto.transfer_time
        )

    @staticmethod
    def from_dtos(dtos: List[TransferRecordDTO]) -> List['TransferResponse']:
        """
        Converts a list of TransferRecordDTO to a list of TransferResponse.
        """
        return [TransferResponse.from_dto(dto) for dto in dtos]

