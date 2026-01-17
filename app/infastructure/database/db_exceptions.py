class DataBaseException(Exception):
    def __init__(self, details: str) -> None:
        super().__init__(details)


class ObjectNotFoundError(DataBaseException): ...


class ObjectAlreadyExistsError(DataBaseException): ...


class EmptyUpdateError(DataBaseException): ...


class UnsafeDeleteError(DataBaseException): ...
