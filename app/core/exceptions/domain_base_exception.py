class DomainBaseException(Exception):
    """
    Domain Base Exception
    """

    status_code: int = 500

    def __init__(
        self,
        message: str,
        details: str | None = None,
    ) -> None:
        self.message = message
        self.details = details
        super().__init__(message)
