from logging import INFO
from logging import basicConfig
from logging import error
from logging import info
from sys import argv

from .browser import get_youtube_url
from .daemon import start_daemon
from .db import db_connection


def daemon() -> None:
    with db_connection() as db:
        start_daemon(db)


def append(args: list[str]) -> None:
    if len(args) not in (2, 3):
        error('usage: "artist" "title"\n   or: --daemon')
        raise SystemExit(-1)

    artist, title = (arg.capitalize() for arg in args)
    youtube_url = get_youtube_url(artist, title)
    with db_connection() as db:
        db.append(artist, title, youtube_url)
        info('inserted %s - %s', artist, title)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    args = argv[1:]

    if len(args) > 0 and args[0] == '--daemon':
        return daemon()

    return append(args)
