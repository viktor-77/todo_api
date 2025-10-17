from typing import Optional


class RepositoryError(Exception):
    """Base repository error."""
    DEFAULT_MESSAGE = "internal error"

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or self.DEFAULT_MESSAGE)


class NotFoundError(RepositoryError):
    DEFAULT_MESSAGE = "resource not found"


class UniqueViolationError(RepositoryError):
    DEFAULT_MESSAGE = "unique constraint violated"


class InvalidIdError(RepositoryError):
    DEFAULT_MESSAGE = "invalid id format"
