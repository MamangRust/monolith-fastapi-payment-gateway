from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Optional


from internal.services.topup_service.domain.dtos.record.user import UserRecordDTO
from internal.services.topup_service.domain.repository.user import IUserRepository
from internal.lib.model.user import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, user_id: int) -> Optional[UserRecordDTO]:
        result = await self.session.execute(select(User).filter(User.user_id == user_id))
        user = result.scalars().first()
        return UserRecordDTO.from_orm(user) if user else None
        