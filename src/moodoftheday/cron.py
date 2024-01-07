from collections.abc import Callable
from datetime import timedelta
from logging import exception
from logging import info
from sched import scheduler
from types import MappingProxyType
from typing import Final
from typing import ParamSpec

from .db import Db
from .db import RowNotFoundError
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
        action(*argument, **kwargs)
        if times is not None and times <= 0:
            return
        s.enter(delay, priority, step, (None if times is None else times - 1,))

    step(times)


def step(db: Db) -> None:
    try:
        id_, artist, title, youtube_url = db.new_row()
    except RowNotFoundError:
        exception('row not found')
    else:
        msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
        publish(msg)
        info('published %s', msg)
        db.mark_row(id_)


def serve_cron(
    db: Db,
    *,
    delay: float = DELAY,
    times: int | None = None,
    blocking: bool = False,
) -> None:
    s = scheduler()
    loop_forever(s, delay, 0, step, (db,), times=times)
    s.run(blocking=blocking)
