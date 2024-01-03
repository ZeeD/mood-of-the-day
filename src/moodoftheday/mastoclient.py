from typing import TypedDict

from dotenv import dotenv_values
from mastodon import Mastodon


class Config(TypedDict):
    client_id: str
    client_secret: str
    access_token: str
    api_base_url: str


def defined(value: str | None) -> str:
    assert value is not None
    return value


def get_config_from_dotenv() -> Config:
    config = dotenv_values()
    return Config(
        client_id=defined(config['client_id']),
        client_secret=defined(config['client_secret']),
        access_token=defined(config['access_token']),
        api_base_url=defined(config['api_base_url']),
    )


def publish(msg: str, config: Config | None = None) -> None:
    cfg = config if config is not None else get_config_from_dotenv()
    Mastodon(**cfg).toot(msg)
