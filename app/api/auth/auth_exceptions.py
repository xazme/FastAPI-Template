class AuthBaseException(Exception):
    def __init__(self, details: str) -> None:
        super().__init__(details)


class PasswordIsIncorrectException(AuthBaseException):
    """Password is incorrect"""


class AccountAlreadyExists(AuthBaseException):
    """Account already exists"""


class RefreshTokenCompromisedException(AuthBaseException):
    """Refresh token is invalid or has been used"""


class NotAuthenticatedException(AuthBaseException):
    """Not Authenticated"""


class EmptyTokenProvidedException(AuthBaseException):
    """Empty token provided"""


class NotEnoughtPermissionsException(AuthBaseException):
    """Not Enough Permissions Exception"""
