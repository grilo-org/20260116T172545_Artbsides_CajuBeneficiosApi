from beanie import Document

from api.shared_resources.entities.timestamp import Timestamp


class BaseDocument(Document):
    name: str
    category_code: str


class Merchant(Timestamp, BaseDocument):
    class Settings:
        name = "merchants"
        use_revision = True

        indexes = Timestamp.indexes
