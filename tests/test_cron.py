from datetime import timedelta
from logging import INFO
from logging import basicConfig
from logging import info
from typing import Final
from unittest import TestCase

from moodoftheday.cron import Cron


class StepError(Exception): ...


class Step:
    def __init__(self, min_i: int) -> None:
        self.i = 0
        self.min_i = min_i
        info('init - i=%s, min_i=%s', self.i, self.min_i)

    def __call__(self) -> None:
        self.i += 5
        info('call - i=%s', self.i)
        if self.i > self.min_i:
            msg = 'bum'
            raise StepError(msg)


DELAY: Final = timedelta(seconds=2).total_seconds()


class TestCron(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        basicConfig(level=INFO)

    def test_run_forever(self) -> None:
        step = Step(12)
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
