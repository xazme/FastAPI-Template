from typing import Callable, Optional, TypeVar, ParamSpec, Concatenate, TYPE_CHECKING
from sqlalchemy.exc import (
    SQLAlchemyError,
    OperationalError,
    DatabaseError,
)

if TYPE_CHECKING:
    from .database_helper import DataBaseHelper

P = ParamSpec("P")
R = TypeVar("R")


def db_exception_handler(
    func: Callable[Concatenate["DataBaseHelper", P], R],
) -> Callable[Concatenate["DataBaseHelper", P], Optional[R]]:
    def wrapper(
        self: "DataBaseHelper", *args: P.args, **kwargs: P.kwargs
    ) -> Optional[R]:
        try:
            result = func(self, *args, **kwargs)
            return result
        except OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
        except DatabaseError as e:
            print(f"Общая ошибка базы данных: {e}")
        except SQLAlchemyError as e:
            print(f"Ошибка SQLAlchemy: {e}")

    return wrapper
