from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.exceptions import ExceptionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api.confs.settings import settings
from api.routers.router import router
from api.exceptions.exception_handler import ExceptionHandler


app = FastAPI(
    redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)


app.add_middleware(
    ExceptionMiddleware, handlers={ Exception: ExceptionHandler.throw }
)

app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)


app.include_router(router)


Instrumentator().instrument(app).expose(
    app, tags=["Monitoring"]
)
