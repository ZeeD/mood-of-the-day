from datetime import UTC
from datetime import datetime


def dt(day: int) -> datetime:
    return datetime(2024, 1, day, tzinfo=UTC)
