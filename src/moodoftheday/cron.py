from collections.abc import Callable
from datetime import timedelta
from logging import exception
from logging import info
from sched import scheduler
from time import time
from types import MappingProxyType
from typing import Final
from typing import ParamSpec

from .config import Config
from .db import Db
from .db import RowNotFoundError
from .dt import get_now
from .mastoclient import publish

DELAY: Final = timedelta(days=1).total_seconds()


P = ParamSpec('P')


def loop_forever(  # noqa: PLR0913
    s: scheduler,
    delay: float,
    priority: int,
    action: Callable[P, None],
    argument: P.args = (),
    kwargs: P.kwargs = MappingProxyType({}),
    *,
    times: int | None = None,
) -> None:
    def step(times: int | None) -> None:
        info('step(times: %s)', times)
        if times is not None and times <= 0:
            return
        try:
            action(*argument, **kwargs)
        finally:
            s.enter(
                delay, priority, step, (None if times is None else times - 1,)
            )

    step(times)


def step(db: Db, config: Config) -> None:
    try:
        id_, artist, title, youtube_url = db.new_row()
    except RowNotFoundError:
        exception('row not found')
    else:
        msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
        publish(config, msg)
        info('published %s', msg)
        db.mark_row(id_)


def serve_cron(
    db: Db,
    config: Config,
    *,
    delay: float = DELAY,
    times: int | None = None,
) -> None:
    s = scheduler()
    loop_forever(s, delay, 0, step, (db, config), times=times)
    s.run(blocking=True)


def every_day_at_08_00(
    action: Callable[P, None],
    argument: P.args = (),
    kwargs: P.kwargs = MappingProxyType({}),
    *,
    timefunc: Callable[[], float] = time,
) -> None:
    s = scheduler(timefunc=timefunc)
    now = get_now()
    today_at_08_00 = now.replace(hour=8, minute=0, second=0, microsecond=0)
    next_time = today_at_08_00
    while next_time < now:
        next_time += timedelta(days=1)
    s.enterabs(next_time.timestamp(), 0, action, argument, kwargs)
    s.run(blocking=True)
