import abc
from typing import List, Optional, Any
from domain.dtos.record.user import UserRecordDTO


class IUserRepository(abc.ABC):
    """
    User Repository interface defining operations for user management.
    """

    @abc.abstractmethod
    async def find_by_id(self, session: Any,user_id: int) -> Optional[UserRecordDTO]:
        """
        Find a user by their ID.
        """
        pass