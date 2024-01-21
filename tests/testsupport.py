from datetime import datetime

from moodoftheday.config import Config
from moodoftheday.dt import TZ


def dt(day: int) -> datetime:
    return datetime(2024, 1, day, tzinfo=TZ)


def c(  # noqa: PLR0913
    *,
    client_id: str = '',
    client_secret: str = '',
    access_token: str = '',
    api_base_url: str = '',
    server_origin: str = '',
    sqlfn: str = '',
) -> Config:
    return Config(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=api_base_url,
        server_origin=server_origin,
        sqlfn=sqlfn,
    )
