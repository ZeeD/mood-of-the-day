from unittest import TestCase

from moodoftheday.db import db_connection
from moodoftheday.web import serve_webui
from testsupport import dt


class TestWeb(TestCase):
    def test_serve_webui(self) -> None:
        now = dt(1)
        with db_connection(':memory:', now) as db:
            serve_webui(db)
