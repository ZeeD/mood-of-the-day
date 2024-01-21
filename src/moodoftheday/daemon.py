from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from .cron import serve_cron
from .web import serve_webui

if TYPE_CHECKING:
    from .config import Config
    from .db import Db


def start_daemon(db: Db, config: Config) -> None:
    with ThreadPoolExecutor() as executor:
        executor.submit(serve_webui, db)
        executor.submit(serve_cron, db, config)
