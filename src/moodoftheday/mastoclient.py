from __future__ import annotations

from logging import info
from typing import TYPE_CHECKING

from mastodon import Mastodon

if TYPE_CHECKING:
    from .config import Config


def publish(config: Config, msg: str) -> None:
    info('publish(%s, %s)', config, msg)
    client_id = config['client_id']
    client_secret = config['client_secret']
    access_token = config['access_token']
    api_base_url = config['api_base_url']

    client = Mastodon(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url=api_base_url,
    )
    client.toot(msg)
