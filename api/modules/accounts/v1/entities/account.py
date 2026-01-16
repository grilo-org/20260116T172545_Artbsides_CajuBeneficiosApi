from beanie import Document

from api.shared_resources.entities.timestamp import Timestamp
from api.modules.accounts.v1.entities.account_balance import AccountBalance


class BaseDocument(Document):
    balance: AccountBalance


class Account(Timestamp, BaseDocument):
    class Settings:
        name = "accounts"
        use_revision = True

        indexes = Timestamp.indexes
