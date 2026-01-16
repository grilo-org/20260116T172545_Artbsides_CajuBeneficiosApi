from fastapi import status

from api.exceptions.errors.base_exception import BaseExceptionError


class NotFoundError(BaseExceptionError):
    args: str = "Resource not found"
    status_code: int = status.HTTP_404_NOT_FOUND
