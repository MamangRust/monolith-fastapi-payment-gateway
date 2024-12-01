from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Text, Sequence, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .base import Base



class Saldo(Base):
    __tablename__ = 'saldo'

    saldo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    total_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    withdraw_amount: Mapped[int] = mapped_column(Integer, default=0)
    withdraw_time: Mapped[str] = mapped_column(TIMESTAMP)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', back_populates='saldo')