from fastapi import Request, HTTPException, status
from unittest import mock
from fastapi.responses import JSONResponse

from api.exceptions.exception_handler import ExceptionHandler


class TestExceptionHandler:
    @mock.patch("api.exceptions.exception_handler.Request")
    async def throw_mapped_error_successful_test(self, request: Request) -> None:
        handler = await ExceptionHandler.throw(
            request, HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        )

        assert handler.status_code is status.HTTP_200_OK

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)

    @mock.patch("api.exceptions.exception_handler.Request")
    async def throw_not_mapped_error_successful_test(self, request: Request) -> None:
        handler = await ExceptionHandler.throw(
            request, AttributeError()
        )

        assert handler.status_code is status.HTTP_200_OK

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)
