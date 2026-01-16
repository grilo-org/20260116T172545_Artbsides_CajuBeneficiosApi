from fastapi import status

from api.exceptions.errors.base_exception import BaseExceptionError


class InternalServerError(BaseExceptionError):
    args: str = "An internal error occurred"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
