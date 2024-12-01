from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Text, Sequence, TIMESTAMP, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .base import Base



class Topup(Base):
    __tablename__ = 'topups'

    topup_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    topup_no: Mapped[str] = mapped_column(Text, nullable=False)
    topup_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    topup_method: Mapped[str] = mapped_column(Text, nullable=False)
    topup_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', back_populates='topups')
