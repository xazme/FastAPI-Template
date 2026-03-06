from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from app.api.user import User, UserRole

from .auth_dependencies import get_current_user
from .auth_exceptions import NotEnoughtPermissionsException

if TYPE_CHECKING:
    from app.api.user import User


def required_role(allowed_roles: list[UserRole]):
    async def guard(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in allowed_roles:
            raise NotEnoughtPermissionsException(details="Не достаточно прав")
        return user

    return guard


RequiredRoleUser = Annotated[
    User,
    Depends(required_role([UserRole.USER])),
]
RequiredRoleAdmin = Annotated[
    User,
    Depends(required_role([UserRole.ADMIN])),
]
RequiredRoleForEveryone = Annotated[
    User,
    Depends(required_role([role for role in UserRole])),
]
