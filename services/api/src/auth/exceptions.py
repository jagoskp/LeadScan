from fastapi import HTTPException, status


class AuthException(HTTPException):
    """Base exception for all Authentication errors."""
    pass


class InvalidCredentialsException(AuthException):
    def __init__(self, detail: str = "Incorrect username, email, or password") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(AuthException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenException(AuthException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserAlreadyExistsException(AuthException):
    def __init__(self, message: str = "User with this email or username already exists") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


class UserInactiveException(AuthException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
