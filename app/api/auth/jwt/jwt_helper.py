import jwt
from typing import Any, Optional
from datetime import datetime, timedelta, timezone
from jwt.exceptions import (
    PyJWTError,
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
    InvalidAlgorithmError,
    ImmatureSignatureError,
    InvalidAudienceError,
)
from .jwt_enums import TokenType
from .jwt_exceptions import JWTExpiredError, JWTInvalidError


class JWTHelper:
    """
    A helper class for encoding and decoding JSON Web Tokens (JWT) using asymmetric cryptography.

    This class provides methods to generate and validate access and refresh tokens with separate
    key pairs and expiration times. It supports configurable algorithms and leverages PyJWT
    for cryptographic operations.

    The tokens can be signed using private keys and verified using corresponding public keys,
    supporting secure authentication flows.

    Attributes:
        alogrithm (str): The cryptographic algorithm used for signing/verifying tokens (e.g., 'RS256').
        expire_days (int): Default token expiration in days (used for refresh tokens).
        expire_minutes (int): Default token expiration in minutes (used for access tokens).
        access_public_key (str | bytes): Public key to verify access tokens.
        refresh_public_key (str | bytes): Public key to verify refresh tokens.
        access_private_key (str | bytes): Private key to sign access tokens.
        refresh_private_key (str | bytes): Private key to sign refresh tokens.

    Example:
        >>> jwt_helper = JWTHelper(
        ...     alogrithm="RS256",
        ...     expire_days=7,
        ...     expire_minutes=15,
        ...     access_private_key="...",
        ...     access_public_key="...",
        ...     refresh_private_key="...",
        ...     refresh_public_key="..."
        ... )
        >>> token = jwt_helper.generate_access_token(data={"sub": "123"})
        >>> payload = jwt_helper.decode_access_token(token)
    """

    def __init__(
        self,
        alogrithm: str,
        expire_days: int,
        expire_minutes: int,
        access_public_key: str | bytes,
        refresh_public_key: str | bytes,
        access_private_key: str | bytes,
        refresh_private_key: str | bytes,
    ):
        self.alogrithm = alogrithm
        self.expire_days = expire_days
        self.expire_minutes = expire_minutes
        self.access_public_key = access_public_key
        self.refresh_public_key = refresh_public_key
        self.access_private_key = access_private_key
        self.refresh_private_key = refresh_private_key

    def generate_access_token(
        self,
        data: dict[str, Any],
    ) -> str:
        """
        Generate a signed JWT access token with a short expiration time.

        The token is signed using the access private key and includes an expiration
        based on `expire_minutes`. Standard claims like `exp` (expiration) and `iat` (issued at)
        are automatically added.

        Args:
            data (dict[str, Any]): The payload data to encode in the token (e.g., user ID, roles).

        Returns:
            str: The encoded JWT access token.

        Note:
            This method uses the access key pair and short-lived expiration suitable for
            frequent, short-term authentication.
        """
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.access_private_key,
            expire_minutes=self.expire_minutes,
        )
        return token

    def generate_refresh_token(
        self,
        data: dict[str, Any],
    ) -> str:
        """
        Generate a signed JWT refresh token with a long expiration time.

        The token is signed using the refresh private key and expires after `expire_days`.
        It is intended to be used for obtaining new access tokens without re-authentication.

        Args:
            data (dict[str, Any]): The payload data to encode in the token.

        Returns:
            str: The encoded JWT refresh token.

        Note:
            This method uses the refresh key pair and longer expiration, suitable for
            secure, long-term token renewal.
        """
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.refresh_private_key,
            expire_days=self.expire_days,
        )
        return token

    def decode_access_token(
        self,
        token: str,
    ) -> Optional[dict[str, Any]]:
        """
        Decode and validate a JWT access token.

        Verifies the token's signature using the access public key and checks expiration.
        Returns the token payload if valid.

        Args:
            token (str): The JWT access token string to decode.

        Returns:
            Optional[dict[str, Any]]: The decoded payload as a dictionary if valid, None otherwise.

        Raises:
            JWTExpiredError: If the token has expired.
            JWTInvalidError: If the token is malformed or invalid.
        """
        return self.__decode(
            token=token,
            type=TokenType.ACCESS,
        )

    def decode_refresh_token(
        self,
        token: str,
    ) -> Optional[dict[str, Any]]:
        """
        Decode and validate a JWT refresh token.

        Verifies the token's signature using the refresh public key and checks expiration.
        Returns the token payload if valid.

        Args:
            token (str): The JWT refresh token string to decode.

        Returns:
            Optional[dict[str, Any]]: The decoded payload as a dictionary if valid, None otherwise.

        Raises:
            JWTExpiredError: If the token has expired.
            JWTInvalidError: If the token is malformed or invalid.
        """
        return self.__decode(
            token=token,
            type=TokenType.REFRESH,
        )

    def __decode(
        self,
        token: str,
        type: TokenType,
    ) -> Optional[dict[str, Any]]:
        """
        Internal method to decode and verify a JWT token using the appropriate public key.

        Selects the correct public key based on token type and uses PyJWT to decode.
        Handles various JWT exceptions and raises custom application-level errors.

        Args:
            token (str): The JWT token to decode.
            type (TokenType): The type of token (ACCESS or REFRESH) to determine key usage.

        Returns:
            Optional[dict[str, Any]]: The decoded token payload if valid.

        Raises:
            JWTExpiredError: If the token's signature has expired.
            JWTInvalidError: If the token is invalid due to signature, structure, or claims.
        """
        key = (
            self.access_public_key
            if type == TokenType.ACCESS
            else self.refresh_public_key
        )
        try:
            data = jwt.decode(
                jwt=token,
                algorithms=[self.alogrithm],
                key=key,
            )  # type: ignore
            return data
        except ExpiredSignatureError:
            raise JWTExpiredError("Token expired")
        except (
            InvalidSignatureError,
            DecodeError,
            InvalidAlgorithmError,
            ImmatureSignatureError,
            InvalidAudienceError,
        ):
            raise JWTInvalidError("Invalid token")
        except PyJWTError as e:
            raise JWTInvalidError(f"Token error: {str(e)}")

    def __encode(
        self,
        data: dict[str, Any],
        algorithm: str,
        private_key: str | bytes,
        expire_minutes: int | None = None,
        expire_days: int | None = None,
    ) -> str:
        """
        Internal method to encode a payload into a JWT token with expiration and issued-at claims.

        Signs the token using the provided private key and algorithm. Expiration can be set
        in minutes (for access tokens) or days (for refresh tokens). Defaults to 1 day if neither
        is specified.

        Args:
            data (dict[str, Any]): The payload to encode.
            algorithm (str): The cryptographic algorithm to use.
            private_key (str | bytes): The private key to sign the token.
            expire_minutes (int | None): Expiration time in minutes (optional).
            expire_days (int | None): Expiration time in days (optional).

        Returns:
            str: The signed JWT token string.

        Note:
            The issued-at (`iat`) and expiration (`exp`) claims are automatically added.
        """
        now = datetime.now(timezone.utc)

        if expire_minutes:
            exp = now + timedelta(minutes=expire_minutes)
        elif expire_days:
            exp = now + timedelta(days=expire_days)
        else:
            exp = now + timedelta(days=1)

        data_to_encode = data.copy()
        data_to_encode.update(
            exp=exp,
            iat=now,
        )
        return jwt.encode(  # type: ignore
            payload=data_to_encode,
            key=private_key,
            algorithm=algorithm,
        )
