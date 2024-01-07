from concurrent.futures import ThreadPoolExecutor

from .config import Config
from .cron import serve_cron
from .db import Db
from .web import serve_webui


def start_daemon(db: Db, config: Config) -> None:
    with ThreadPoolExecutor() as executor:
        executor.submit(serve_webui, db)
        executor.submit(serve_cron, db, config)
