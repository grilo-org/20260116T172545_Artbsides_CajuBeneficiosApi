from api.exceptions.errors.base_exception import BaseExceptionError


class TestBaseExceptionError:
    def base_exception_successful_test(self) -> None:
        exception = BaseExceptionError()

        assert not exception.args
        assert not exception.status_code
