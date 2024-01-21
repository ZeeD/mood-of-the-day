from datetime import timedelta
from logging import INFO
from logging import basicConfig
from typing import Final
from unittest import TestCase
from logging import info

from moodoftheday.cron import Cron


class Step:
    def __init__(self) -> None:
        self.i = 0
        info('init - i=%s', self.i)

    def __call__(self) -> None:
        self.i += 5
        info('call - i=%s', self.i)
        if self.i > 12:
            raise Exception('bum')


DELAY: Final = timedelta(seconds=2).total_seconds()


class TestCron(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        basicConfig(level=INFO)

    def test_run_forever(self) -> None:
        step = Step()
        Cron(step).run_forever(
            replace_kwargs={
                'hour': 11,
                'minute': 49,
                'second': 0,
                'microsecond': 0,
            },
            timedelta_kwargs={'seconds': 1.0},
        )
        self.assertEqual(step.i, 15)
