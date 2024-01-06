from collections.abc import Callable
from datetime import timedelta
from logging import exception
from logging import info
from sched import scheduler
from typing import Final
from typing import ParamSpec

from .db import Db
from .db import RowNotFoundError
from .mastoclient import publish

DELAY: Final = timedelta(days=1).total_seconds()


P = ParamSpec('P')


def loop_forever(
    s: scheduler,
    delay: float,
    priority: int,
    action: Callable[P, None],
    argument: P.args,
    kwargs: P.kwargs,
) -> None:
    def step() -> None:
        action(*argument, **kwargs)
        s.enter(delay, priority, step)

    step()


def step(db: Db, s: scheduler, delay: float, next_steps: int | None) -> None:
    try:
        id_, artist, title, youtube_url = db.new_row()
    except RowNotFoundError:
        exception('row not found')
    else:
        msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
        publish(msg)
        info('published %s', msg)
        db.mark_row(id_)
    if next_steps is None or next_steps > 0:
        s.enter(
            delay,
            0,
            step,
            (db, s, delay, None if next_steps is None else next_steps - 1),
        )


def serve_cron(
    db: Db,
    delay: float = DELAY,
    next_steps: int | None = None,
    *,
    blocking: bool = False,
) -> None:
    s = scheduler()
    step(db, s, delay, next_steps)
    s.run(blocking=blocking)
