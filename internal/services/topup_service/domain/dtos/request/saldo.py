from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateSaldoRequest(BaseModel):
    user_id: int
    total_balance: int




class UpdateSaldoBalanceRequest(BaseModel):
    total_balance: int
    user_id: int