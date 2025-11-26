from fastapi import Depends
from typing import Annotated
from app.api.user import User, UserRole
from .auth_dependencies import get_current_user
from .auth_exceptions import NotEnoughtPermissionsException


def required_role(allowed_roles: list[UserRole]):
    async def guard(user: Annotated[User, Depends(get_current_user)]):
        if user.role not in allowed_roles:
            raise NotEnoughtPermissionsException(details="Не достаточно прав")
        return user

    return guard


RequiredRoleStudent = Annotated[
    User,
    Depends(required_role([UserRole.STUDENT])),
]
RequiredRoleLector = Annotated[
    User,
    Depends(required_role([UserRole.LECTOR])),
]
RequiredRoleForEveryone = Annotated[
    User,
    Depends(required_role([role for role in UserRole])),
]
