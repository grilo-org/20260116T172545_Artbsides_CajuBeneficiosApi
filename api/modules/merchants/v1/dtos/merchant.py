from typing import Optional
from pydantic import BaseModel


class MerchantDto:
    class Read:
        class Parameters(BaseModel):
            category_code: Optional[str] = None

    class ReadOne:
        class Parameters(BaseModel):
            name: str
