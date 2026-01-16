from typing import ClassVar, Optional
from pymongo import DESCENDING, IndexModel
from datetime import datetime, timezone


class Timestamp:
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    indexes: ClassVar[list[IndexModel]] = [
        IndexModel(
            [("created_at", DESCENDING)], name="_ca-_"
        ),
        IndexModel(
            [("updated_at", DESCENDING)], name="_ua-_"
        ),
        IndexModel(
            [("deleted_at", DESCENDING)], name="_da-_"
        )
    ]
