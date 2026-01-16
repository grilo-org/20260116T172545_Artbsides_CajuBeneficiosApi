from pydantic import BaseModel
from pydantic_mongo import ObjectIdField

from api.modules.accounts.v1.entities.account_balance import AccountBalance


class AccountDto:
    class ReadOne:
        class Parameters(BaseModel):
            id: ObjectIdField

    class Update:
        class Data(BaseModel):
            balance: AccountBalance
