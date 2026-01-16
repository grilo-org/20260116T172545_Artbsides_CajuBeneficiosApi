from beanie import PydanticObjectId, DecimalAnnotation
from typing import Literal
from pydantic import Field, BaseModel, RootModel, model_serializer

from api.modules.transactions.v1.enums.transaction_code import TransactionCode


class AuthorizerDto:
    class Data(BaseModel):
        account_id: PydanticObjectId = Field(alias="account")
        price: DecimalAnnotation = Field(decimal_places=2, alias="totalAmount")
        category_code: str = Field(alias="mcc")
        merchant: str

    class Parameters(BaseModel):
        fallback: bool = False

    class Response(RootModel):
        root: TransactionCode

        @model_serializer
        def serialize_model(self) -> dict[Literal["code"], TransactionCode]:
            return {
                "code": self.root
            }
