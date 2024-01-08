from datetime import timedelta
from logging import INFO
from logging import basicConfig
from sched import scheduler
from typing import Final
from unittest import TestCase

from moodoftheday.cron import loop_forever


class Step:
    def __init__(self) -> None:
        self.i = 0

    def __call__(self) -> None:
        self.i += 5


DELAY: Final = timedelta(seconds=2).total_seconds()


class TestConfig(TestCase):
    def test_loop_forever(self) -> None:
        basicConfig(level=INFO)
        step = Step()
        s = scheduler()
        loop_forever(s, DELAY, 0, step, times=3)
        s.run(blocking=True)
        self.assertEqual(step.i, 15)
