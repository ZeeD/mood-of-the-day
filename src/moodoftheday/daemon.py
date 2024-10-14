from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from moodoftheday.cron import serve_cron
from moodoftheday.web import serve_webui

if TYPE_CHECKING:
    from moodoftheday.config import Config
    from moodoftheday.db import Db


def start_daemon(db: 'Db', config: 'Config') -> None:
    with ThreadPoolExecutor() as executor:
        executor.submit(serve_webui, db)
        executor.submit(serve_cron, db, config)
