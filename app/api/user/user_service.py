from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import BaseService, BaseRepository
from .user_model import User


class UserService(BaseService[User]):
    def __init__(self, repository: BaseRepository[User], session: AsyncSession) -> None:
        super().__init__(repository=repository, session=session)
