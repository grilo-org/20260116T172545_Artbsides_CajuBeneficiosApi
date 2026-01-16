from fastapi import status

from api.exceptions.errors.base_exception import BaseExceptionError


class MethodNotAllowedError(BaseExceptionError):
    args: str = "Method not allowed"
    status_code: int = status.HTTP_405_METHOD_NOT_ALLOWED
