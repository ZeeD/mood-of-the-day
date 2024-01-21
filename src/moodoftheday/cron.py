from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from logging import exception
from logging import info
from sched import scheduler
from time import time
from typing import TYPE_CHECKING
from typing import Any

from .db import RowNotFoundError
from .dt import TZ
from .mastoclient import publish

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from .config import Config
    from .db import Db


class Cron(scheduler):
    def __init__(
        self,
        action: Callable[..., None],
        args: tuple[Any, ...] = (),
        kwargs: Mapping[str, Any] = {},
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
                exception('exception in action')

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
        now = datetime.fromtimestamp(self.timefunc(), TZ)
        dt = now.replace(**replace_kwargs)  # today, at 08:00
        while dt <= now:
            dt += timedelta(**timedelta_kwargs)
        return dt.timestamp()


def _serve_cron_step(db: Db, config: Config) -> None:
    try:
        id_, artist, title, youtube_url = db.new_row()
    except RowNotFoundError:
        exception('row not found')
    else:
        msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
        publish(config, msg)
        info('published %s', msg)
        db.mark_row(id_)


def serve_cron(db: Db, config: Config) -> None:
    Cron(_serve_cron_step, (db, config)).run_forever()
