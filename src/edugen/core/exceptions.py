class EduGenError(Exception):
    """Base error for EduGen AI."""


class ValidationError(EduGenError, ValueError):
    """Raised when user input fails validation."""


class StorageError(EduGenError):
    """Raised when persistence fails."""


def format_error(error: Exception) -> str:
    return f"{error.__class__.__name__}: {error}"
