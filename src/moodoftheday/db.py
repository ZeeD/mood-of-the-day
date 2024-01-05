from __future__ import annotations

from contextlib import contextmanager
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

if TYPE_CHECKING:
    from collections.abc import Iterator


SQLFN: Final = Path('~/moodoftheday.sqlite').expanduser()


register_adapter(datetime, lambda dt: dt.timestamp())
register_converter(
    'timestamp', lambda ts: datetime.fromtimestamp(float(ts), tz=UTC)
)


def create_schema(connection: Connection) -> None:
    cursor = connection.cursor()
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
    connection.commit()


class Db:
    def __init__(self, now: datetime, connection: Connection) -> None:
        self.now = now
        self.connection = connection

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

    def all_rows(
        self,
    ) -> Iterator[tuple[int, str, str, str, datetime, datetime]]:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            select id, artist, title, youtube_url, creation_date, published_date
            from moods
            order by creation_date
            """
        )
        for row in cursor.fetchall():
            (
                id_,
                artist,
                title,
                youtube_url,
                creation_date,
                published_date,
            ) = row
            yield (
                id_,
                artist,
                title,
                youtube_url,
                creation_date,
                published_date,
            )


@contextmanager
def db_connection(
    sqlfn: Path | str = SQLFN, now: datetime | None = None
) -> Iterator[Db]:
    connection = connect(sqlfn, detect_types=PARSE_DECLTYPES)
    try:
        create_schema(connection)
        yield Db(now if now is not None else datetime.now(tz=UTC), connection)
    finally:
        connection.close()
