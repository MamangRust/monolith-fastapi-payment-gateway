from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Text, Sequence, TIMESTAMP, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class Transfer(Base):
    __tablename__ = 'transfers'

    transfer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transfer_from: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    transfer_to: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    transfer_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transfer_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user_from = relationship('User', foreign_keys=[transfer_from], back_populates='transfers_from')
    user_to = relationship('User', foreign_keys=[transfer_to], back_populates='transfers_to')
