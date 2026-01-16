from fastapi import status

from api.exceptions.errors.unauthorized_token import UnauthorizedTokenError


class TestUnauthorizedTokenError:
    def unauthorized_token_error_successful_test(self) -> None:
        exception = UnauthorizedTokenError()

        assert exception.args is not None
        assert exception.status_code is status.HTTP_403_FORBIDDEN
