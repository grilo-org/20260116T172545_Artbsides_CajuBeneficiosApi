import logging
import importlib
import inflection

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from api.exceptions.errors.base_exception import BaseExceptionError
from api.exceptions.errors.internal_server import InternalServerError
from api.modules.transactions.v1.dtos.authorizer import AuthorizerDto
from api.modules.transactions.v1.enums.transaction_code import TransactionCode


logger = logging.getLogger("uvicorn.error")


class ExceptionHandler:
    @staticmethod
    async def throw(_: Request, exception: BaseExceptionError) -> JSONResponse:
        module = "HTTPExceptionError" if isinstance(exception, HTTPException) \
            else type(exception).__name__

        try:
            exception = getattr(importlib.import_module(
                f"api.exceptions.errors.{ inflection.underscore(module).replace("_error", "") }"), module)(exception)
        except:
            exception = InternalServerError

        if status_code := getattr(exception, "status_code", ""):
            status_code = f" {status_code}"

        logger.error("%s%s, %s", module,
            status_code, exception.args or "Not mapped exception", exc_info=True
        )

        return JSONResponse(
            AuthorizerDto.Response(root=TransactionCode.failure).model_dump(), status.HTTP_200_OK
        )
