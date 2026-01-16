from fastapi import status

from api.exceptions.errors.base_exception import BaseExceptionError


class UnauthorizedTokenError(BaseExceptionError):
    args: str = "Check your bearer token, you might not be authorized"
    status_code: int = status.HTTP_403_FORBIDDEN
