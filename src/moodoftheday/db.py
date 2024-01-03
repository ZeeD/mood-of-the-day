from __future__ import annotations

from contextlib import AbstractContextManager
from datetime import UTC
from datetime import datetime
from pathlib import Path
from sqlite3 import PARSE_DECLTYPES
from sqlite3 import Connection
from sqlite3 import connect
from sqlite3 import register_adapter
from sqlite3 import register_converter
from typing import TYPE_CHECKING
from typing import Final
from typing import Self
from typing import override

if TYPE_CHECKING:
    from types import TracebackType

SQLFN: Final = Path('~/moodoftheday.sqlite').expanduser()


register_adapter(datetime, lambda dt: dt.timestamp())
register_converter(
    'timestamp', lambda ts: datetime.fromtimestamp(int(ts), tz=UTC)
)


class Db(AbstractContextManager['Db']):
    connection: Connection

    def __init__(
        self, now: datetime | None = None, sqlfn: Path | str = SQLFN
    ) -> None:
        self.now = now if now is not None else datetime.now(tz=UTC)
        self.sqlfn = sqlfn

    @override
    def __enter__(self) -> Self:
        self.connection = connect(self.sqlfn, detect_types=PARSE_DECLTYPES)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            create table if not exists moods(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT,
                title TEXT,
                youtube_url TEXT,
                creation_date timestamp,
                published_date timestamp
            )
            """
        )
        self.connection.commit()
        return self

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.connection.close()
        return super().__exit__(exc_type, exc_value, traceback)

    def append(self, artist: str, title: str, youtube_url: str) -> int | None:
        cursor = self.connection.cursor()
        # TODO: check duplicates
        cursor.execute(
            """
            insert into moods(artist, title, youtube_url, creation_date)
            values (?,?,?,?)
            """,
            (artist, title, youtube_url, self.now),
        )
        self.connection.commit()
        return cursor.lastrowid

    def new_row(self) -> tuple[int, str, str, str]:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            select id, artist, title, youtube_url
            from moods
            where published_date is null
            order by creation_date
            """
        )
        row = cursor.fetchone()
        if row is None:
            raise SystemExit
        (id_, artist, title, youtube_url) = row
        return (id_, artist, title, youtube_url)

    def mark_row(self, id_: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            update moods set published_date=?
            where id=?
            """,
            (self.now, id_),
        )
        self.connection.commit()
