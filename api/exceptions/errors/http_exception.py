from fastapi import status
from starlette.exceptions import HTTPException

from api.exceptions.errors.not_found import NotFoundError
from api.exceptions.errors.base_exception import BaseExceptionError
from api.exceptions.errors.internal_server import InternalServerError
from api.exceptions.errors.method_not_allowed import MethodNotAllowedError


class HTTPExceptionError(BaseExceptionError):
    def __new__(cls, exception: HTTPException) -> Exception:
        match exception.status_code:
            case status.HTTP_404_NOT_FOUND:
                return NotFoundError
            case status.HTTP_405_METHOD_NOT_ALLOWED:
                return MethodNotAllowedError

        raise InternalServerError from exception
