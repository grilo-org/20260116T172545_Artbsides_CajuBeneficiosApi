from typing import Optional


class BaseExceptionError(Exception):
    args: Optional[str] = None
    status_code: Optional[int] = None
