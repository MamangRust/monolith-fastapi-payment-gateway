from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional

from internal.services.auth_service.domain.dtos.request.user import CreateUserRequest, UpdateUserRequest
from internal.services.auth_service.domain.dtos.record.user import UserRecordDTO
from internal.services.auth_service.domain.repository.user import IUserRepository

from internal.lib.model.user import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: CreateUserRequest) -> UserRecordDTO:
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password=user.password,
            noc_transfer=user.noc_transfer,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserRecordDTO.from_orm(new_user)

    async def find_by_email_exists(self, email: str) -> bool:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return user is not None

    async def find_by_email(self, email: str) -> Optional[UserRecordDTO]:
        result = await self.session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        return UserRecordDTO.from_orm(user) if user else None
