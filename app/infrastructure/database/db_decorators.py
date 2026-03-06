from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    ParamSpec,
    TypeVar,
)

from sqlalchemy.exc import (
    DatabaseError,
    OperationalError,
    SQLAlchemyError,
)

from .db_infrastructure_exceptions import (
    DBDatabaseError,
    DBOperationalError,
    DBSQLAlchemyError,
)

if TYPE_CHECKING:
    from .db_helper import DataBaseHelper

P = ParamSpec("P")
R = TypeVar("R")


def db_exception_handler(
    func: Callable[Concatenate["DataBaseHelper", P], Awaitable[R]],
) -> Callable[Concatenate["DataBaseHelper", P], Coroutine[Any, Any, R | None]]:
    @wraps(func)
    async def wrapper(
        self: "DataBaseHelper", *args: P.args, **kwargs: P.kwargs
    ) -> R | None:
        try:
            return await func(self, *args, **kwargs)

        except OperationalError as e:
            raise DBOperationalError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

        except DatabaseError as e:
            raise DBDatabaseError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

        except SQLAlchemyError as e:
            raise DBSQLAlchemyError(
                model_name=self.__class__.__name__,
                details=str(e),
            ) from e

    return wrapper
