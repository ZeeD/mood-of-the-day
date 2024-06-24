from datetime import datetime
from typing import Final
from zoneinfo import ZoneInfo

TZ: Final = ZoneInfo('Europe/Rome')


def get_now(now: datetime | None = None) -> datetime:
    return now if now is not None else datetime.now(tz=TZ)


def from_timestamp(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, tz=TZ)
