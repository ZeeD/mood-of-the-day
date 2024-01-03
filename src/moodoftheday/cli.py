from logging import INFO
from logging import basicConfig
from logging import error
from logging import info
from sys import argv

from .browser import get_youtube_url
from .db import Db
from .mastoclient import publish


def cron() -> None:
    # called by cron
    with Db() as db:
        id_, artist, title, youtube_url = db.new_row()
        msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
        publish(msg)
        info('published %s', msg)
        db.mark_row(id_)


def append(args: list[str]) -> None:
    # called by user

    if len(args) not in (2, 3):
        error('usage: "artist" "title"\n   or: --cron')
        raise SystemExit(-1)

    artist, title = (arg.capitalize() for arg in args)
    youtube_url = get_youtube_url(artist, title)
    with Db() as db:
        db.append(artist, title, youtube_url)
        info('inserted %s - %s', artist, title)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    args = argv[1:]
    if len(args) > 0 and args[0] == '--cron':
        return cron()

    return append(args)
