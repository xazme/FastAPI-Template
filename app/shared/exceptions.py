class RepositoryError(Exception):
    """Базовое исключение для всех ошибок репозитория"""


class ObjectNotFoundError(RepositoryError):
    """Объект не найден"""


class ObjectAlreadyExistsError(RepositoryError):
    """Нарушение уникальности"""


class EmptyUpdateError(RepositoryError):
    """Попытка вызвать update без payload"""


class UnsafeDeleteError(RepositoryError):
    """Попытка удалить без фильтров"""
