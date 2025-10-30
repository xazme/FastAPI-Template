from sqlalchemy.ext.asyncio import AsyncSession
from shared.base_repository import BaseRepository
from shared import BaseService
from .user_model import User


class UserService(BaseService[User]):
    def __init__(self, repository: BaseRepository[User], session: AsyncSession) -> None:
        super().__init__(repository=repository, session=session)
