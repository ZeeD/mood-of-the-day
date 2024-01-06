from logging import INFO
from logging import basicConfig
from logging import error
from logging import exception
from logging import info
from sys import argv

from .browser import get_youtube_url
from .db import RowNotFoundError
from .db import db_connection
from .mastoclient import publish
from .web import serve_webui


def cron() -> None:
    # called by cron
    with db_connection() as db:
        try:
            id_, artist, title, youtube_url = db.new_row()
        except RowNotFoundError:
            exception('row not found')
        else:
            msg = f'Mood of the day: {artist} - {title}\n\n{youtube_url}'
            publish(msg)
            info('published %s', msg)
            db.mark_row(id_)


def webui() -> None:
    with db_connection() as db:
        serve_webui(db)


def append(args: list[str]) -> None:
    # called by user

    if len(args) not in (2, 3):
        error('usage: "artist" "title"\n   or: --cron')
        raise SystemExit(-1)

    artist, title = (arg.capitalize() for arg in args)
    youtube_url = get_youtube_url(artist, title)
    with db_connection() as db:
        db.append(artist, title, youtube_url)
        info('inserted %s - %s', artist, title)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    args = argv[1:]

    if len(args) > 0 and args[0] == '--cron':
        return cron()

    if len(args) > 0 and args[0] == '--web':
        return webui()

    return append(args)
