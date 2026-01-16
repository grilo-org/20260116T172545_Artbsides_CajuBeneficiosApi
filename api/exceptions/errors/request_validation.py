from fastapi import status
from fastapi.exceptions import RequestValidationError as FastApiRequestValidationError


class RequestValidationError(FastApiRequestValidationError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, exception: FastApiRequestValidationError) -> None:
        self.args = exception.errors()
