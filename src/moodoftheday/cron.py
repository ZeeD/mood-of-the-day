from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from logging import INFO
from logging import basicConfig
from logging import exception
from logging import info
from sched import scheduler
from time import time
from typing import Any
from typing import Callable
from typing import Mapping

from zoneinfo import ZoneInfo


def action(*args: Any, **kwargs: Any) -> None:
    info('action(%s, %s)', args, kwargs)


class Cron(scheduler):
    def __init__(
        self,
        action: Callable[..., None],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        super().__init__(timefunc=time)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def run_forever(
        self,
        /,
        *,
        replace_kwargs: Mapping[str, Any] = {
            'hour': 8,
            'minute': 0,
            'second': 0,
            'microsecond': 0,
        },
        timedelta_kwargs: Mapping[str, float] = {'days': 1.0},
    ) -> None:
        self._step(replace_kwargs, timedelta_kwargs, first_time=True)
        super().run(blocking=True)

    def _step(
        self,
        replace_kwargs: Mapping[str, Any],
        timedelta_kwargs: Mapping[str, float],
        *,
        first_time: bool,
    ) -> None:
        if not first_time:
            try:
                self.action(*self.args, **self.kwargs)
            except Exception:
                exception('')

        self.enterabs(
            self._next(replace_kwargs, timedelta_kwargs),
            0,
            self._step,
            (replace_kwargs, timedelta_kwargs),
            {'first_time': False},
        )

    def _next(
        self,
        replace_kwargs: Mapping[str, Any],
        timedelta_kwargs: Mapping[str, float],
    ) -> float:
        now = datetime.fromtimestamp(self.timefunc(), ZoneInfo('Europe/Rome'))
        dt = now.replace(**replace_kwargs)  # today, at 08:00
        while dt <= now:
            dt += timedelta(**timedelta_kwargs)
        return dt.timestamp()


def main() -> None:
    basicConfig(level=INFO, format='%(asctime)s\n\t%(message)s')
    Cron(action, ('foo', 'bar'), {'baz': 'qux'}).run_forever(
        replace_kwargs={
            'hour': 12,
            'minute': 33,
            'second': 0,
            'microsecond': 0,
        },
        timedelta_kwargs={'seconds': 3.0},
    )


if __name__ == '__main__':
    main()
