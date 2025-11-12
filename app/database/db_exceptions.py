class DataBaseException(Exception):
    def __init__(self, details: str) -> None:
        super().__init__(details)


class ObjectNotFoundError(DataBaseException):
    """Объект не найден"""


class ObjectAlreadyExistsError(DataBaseException):
    """Нарушение уникальности"""


class EmptyUpdateError(DataBaseException):
    """Попытка вызвать update без payload"""


class UnsafeDeleteError(DataBaseException):
    """Попытка удалить без фильтров"""
