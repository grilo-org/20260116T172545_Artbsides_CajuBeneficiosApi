import jwt
import pytest

from fastapi import Request, status
from datetime import datetime, timezone, timedelta
from unittest import mock

from api.confs.settings import settings
from api.utils.authorization import Authorization
from api.exceptions.errors.unauthorized_token import UnauthorizedTokenError


class TestAuthorization:
    token = jwt.encode(
        key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM, payload={
            "exp": (datetime.now(timezone.utc) + timedelta(seconds=30)).timestamp()
        }
    )

    @mock.patch("api.utils.authorization.Request")
    async def authorization_successful_test(self, request: Request) -> None:
        request.headers = {
            "Authorization": f"Bearer {self.token}"
        }

        assert await Authorization().__call__(request) is None

    @mock.patch("api.utils.authorization.Request")
    async def authorization_failure_test(self, request: Request) -> None:
        request.headers = {
            "Authorization": "Bearer invalid_token"
        }

        with pytest.raises(UnauthorizedTokenError) as exception:
            await Authorization().__call__(request)

        assert exception.value.args is not None
        assert exception.value.status_code is status.HTTP_403_FORBIDDEN
