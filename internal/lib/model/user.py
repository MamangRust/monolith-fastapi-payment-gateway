from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Text, Sequence, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    noc_transfer: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, default="0")
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    topups = relationship('Topup', back_populates='user')
    saldo = relationship('Saldo', back_populates='user')
    transfers_from = relationship('Transfer', foreign_keys='Transfer.transfer_from', back_populates='user_from')
    transfers_to = relationship('Transfer', foreign_keys='Transfer.transfer_to', back_populates='user_to')
    withdraws = relationship('Withdraw', back_populates='user')

    def as_dict(self):
        # Exclude 'password' from the dictionary
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' and k != 'password'}



