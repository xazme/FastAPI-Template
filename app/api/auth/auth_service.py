from uuid import UUID
from typing import TYPE_CHECKING
from app.api.user.user_enums import UserRole
from app.api.user.user_service import UserService
from app.api.token.token_dto import UpsertTokenDTO
from app.api.token.token_service import TokenService
from .jwt import JWTHelper
from .utils import PasswordHasher
from .auth_dto import (
    LoginDTO,
    RegisterDTO,
    LogOutDTO,
    ResponseAuthTokensDTO,
    RefreshTokenDTO,
)
from .auth_exceptions import (
    PasswordIsIncorrectException,
    AccountAlreadyExists,
    RefreshTokenCompromisedException,
)

if TYPE_CHECKING:
    from app.api.user import User


class AuthService:
    """
    Service class responsible for handling authentication-related operations.

    This service manages user login, registration, token refresh, and logout flows.
    It uses dependency-injected components for JWT handling, password hashing,
    token persistence, and user management. It ensures secure authentication
    by validating credentials, generating tokens, and maintaining token state.

    Dependencies:
        jwt_helper (JWTHelper): For encoding and decoding JWT access and refresh tokens.
        password_hasher (PasswordHasher): For securely hashing and verifying passwords.
        token_service (TokenService): For storing, retrieving, and deleting refresh tokens.
        user_service (UserService): For user creation and retrieval operations.

    Example:
        >>> auth_service = AuthService(jwt_helper, password_hasher, token_service, user_service)
        >>> tokens = await auth_service.login(LoginDTO(email="user@example.com", password="pass"))

    Note:
        This class assumes that DTOs (Data Transfer Objects) are used for input validation
        and that UUIDs are used as primary keys for users.
    """

    def __init__(
        self,
        jwt_helper: JWTHelper,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        user_service: UserService,
    ) -> None:
        self.jwt_helper = jwt_helper
        self.password_hasher = password_hasher
        self.user_service = user_service
        self.token_service = token_service

    async def login(
        self,
        payload: LoginDTO,
    ) -> ResponseAuthTokensDTO:
        """
        Authenticate a user using email and password.

        Validates the provided credentials against the stored user data.
        If valid, generates new access and refresh tokens and saves the refresh token.

        Args:
            payload (LoginDTO): Contains the user's email and password.

        Returns:
            ResponseAuthTokensDTO: A DTO containing the new access and refresh tokens.

        Raises:
            PasswordIsIncorrectException: If the email does not exist or the password is incorrect.
        """
        user_email = payload.email
        user = await self.user_service.get_one_or_none(email=user_email)

        if not user or not self.password_hasher.check(
            password=payload.password,
            password_hash=user.password,
        ):
            raise PasswordIsIncorrectException(details="Incorrect email or password")
        return await self._create_and_save_token(user_id=user.id)

    async def register(
        self,
        payload: RegisterDTO,
    ) -> ResponseAuthTokensDTO:
        """
        Register a new user with the provided data.

        Checks if a user with the given email already exists. If not, hashes the password,
        creates a new user with default role (STUDENT), and issues authentication tokens.

        Args:
            payload (RegisterDTO): Contains user registration data including email and password.

        Returns:
            ResponseAuthTokensDTO: A DTO containing access and refresh tokens for the new user.

        Raises:
            AccountAlreadyExists: If a user with the provided email already exists.
        """
        existing_user = await self.user_service.get_one_or_none(email=payload.email)
        if existing_user:
            raise AccountAlreadyExists("Account Already Exists")

        hashed_password = self.password_hasher.get(payload.password)
        user_data = payload.model_dump()
        user_data.update(
            {
                "password": hashed_password,
                "role": UserRole.STUDENT,
            }
        )
        user = await self.user_service.create(payload=user_data)
        return await self._create_and_save_token(user_id=user.id)

    async def logout(
        self,
        payload: LogOutDTO,
    ) -> None:
        """
        Log out a user by deleting their stored refresh token.

        Invalidates the current refresh token, preventing future token renewal.

        Args:
            payload (LogOutDTO): Contains the user ID to log out.

        Returns:
            None
        """
        await self.token_service.delete(user_id=payload.user_id)

    async def refresh_token(
        self,
        payload: RefreshTokenDTO,
    ) -> ResponseAuthTokensDTO:
        """
        Generate new tokens using a valid refresh token.

        Validates the refresh token against the database and JWT rules.
        If valid, issues a new pair of access and refresh tokens.
        If invalid or compromised, deletes the token and raises an exception.

        Args:
            payload (RefreshTokenDTO): Contains the current refresh token.

        Returns:
            ResponseAuthTokensDTO: A DTO with new access and refresh tokens.

        Raises:
            RefreshTokenCompromisedException: If the refresh token is invalid, not found, or has been tampered with.
        """
        data = self.jwt_helper.decode_refresh_token(token=payload.refresh_token)
        user_id: str = data.get("user_id")  # type: ignore
        db_token = await self.token_service.get_one_or_none(user_id=user_id)
        if (
            not db_token
            or db_token.refresh_token != payload.refresh_token
            or not db_token.refresh_token
        ):
            await self.token_service.delete(refresh_token=payload.refresh_token)
            raise RefreshTokenCompromisedException(
                details="Refresh token is invalid or has been used"
            )
        return await self._create_and_save_token(user_id=UUID(user_id))

    async def _create_and_save_token(
        self,
        user_id: UUID,
    ) -> ResponseAuthTokensDTO:
        """
        Internal method to generate and persist new authentication tokens for a user.

        Creates JWT access and refresh tokens, then stores the refresh token in the database
        (or updates it if already exists).

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            ResponseAuthTokensDTO: A DTO containing the newly generated access and refresh tokens.
        """
        jwt_payload = {"user_id": str(user_id)}
        access_token = self.jwt_helper.generate_access_token(data=jwt_payload)
        refresh_token = self.jwt_helper.generate_refresh_token(data=jwt_payload)

        await self.token_service.upsert(
            payload=UpsertTokenDTO(user_id=user_id, refresh_token=refresh_token)
        )
        return ResponseAuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_user_from_access_token(
        self,
        access_token: str,
    ) -> "User":
        """
        Retrieve the user associated with a valid access token.

        Decodes the access token to extract the user ID, then fetches the full user
        record from the database.

        Args:
            access_token (str): The JWT access token string.

        Returns:
            User: The user instance corresponding to the token.

        Raises:
            JWTExpiredError or JWTInvalidError: If the token is expired or invalid.
            UserNotFound: If no user exists with the extracted ID.
        """
        payload = self.jwt_helper.decode_access_token(token=access_token)
        user_id: str = payload.get("user_id")  # type: ignore
        user: "User" = await self.user_service.get_one(id=UUID(user_id))
        return user
