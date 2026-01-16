from datetime import datetime, timezone

from api.shared_resources.entities.timestamp import Timestamp


class TestTimestamp:
    def timestamp_success_test(self) -> None:
        timestamp = Timestamp()

        assert isinstance(timestamp.created_at, datetime)
        assert timestamp.created_at.tzinfo == timezone.utc

        assert not timestamp.updated_at
        assert not timestamp.deleted_at

        assert timestamp.indexes is not None
