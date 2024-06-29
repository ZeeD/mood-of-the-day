from unittest import TestCase

from _support.factories import c
from moodoftheday.db import db_connection
from moodoftheday.web import serve_webui


class TestWeb(TestCase):
    def test_serve_webui(self) -> None:
        with db_connection(c(sqlfn=':memory:')) as db:
            serve_webui(db, open_browser=True)
