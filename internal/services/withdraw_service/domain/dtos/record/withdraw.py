from pydantic import BaseModel
from datetime import datetime

class WithdrawRecordDTO(BaseModel):
    withdraw_id: int
    user_id: int
    withdraw_amount: int
    withdraw_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True