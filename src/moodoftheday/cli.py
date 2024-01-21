from __future__ import annotations

from logging import INFO
from logging import basicConfig
from logging import error
from sys import argv

from .config import get_config
from .daemon import start_daemon
from .db import db_connection
from .web import client_append


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    config = get_config()

    name, *args = argv
    if args and args[0] == '--daemon':
        with db_connection(config) as db:
            start_daemon(db, config)

    if len(args) not in (2, 3):
        error('usage: %s "artist" "title"\n   or: --daemon', name)
        raise SystemExit(-1)

    artist, title = args
    client_append(config, artist, title)
