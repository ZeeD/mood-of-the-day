from datetime import UTC
from datetime import datetime
from unittest import TestCase

from moodoftheday.db import Db


def dt(day: int) -> datetime:
    return datetime(2024, 1, day, tzinfo=UTC)


class TestDb(TestCase):
    def test_empty(self) -> None:
        now = dt(1)
        with Db(now, ':memory:') as db:
            db.append('foo', 'bar', 'baz')
            id_, artist, title, youtbe_url = db.new_row()
            self.assertEqual(artist, 'foo')
            self.assertEqual(title, 'bar')
            self.assertEqual(youtbe_url, 'baz')
            db.mark_row(id_)

            cursor = db.connection.cursor()
            cursor.execute(
                """
            select id,
                   artist, title, youtube_url,
                   creation_date, published_date
            from moods
            """
            )
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 1)
            [row] = rows
            self.assertEqual(row[1], 'foo')
            self.assertEqual(row[2], 'bar')
            self.assertEqual(row[3], 'baz')
            self.assertEqual(row[4], now)
            self.assertEqual(row[5], now)
