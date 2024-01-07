from pathlib import Path
from typing import Final
from typing import TypedDict

from dotenv import dotenv_values


class Config(TypedDict):
    client_id: str
    client_secret: str
    access_token: str
    api_base_url: str
    server_origin: str
    sqlfn: str


def defined(value: str | None) -> str:
    assert value is not None
    return value


DOTENV_PATH: Final = Path(__file__).parent.parent.with_name(
    'mood-of-the-day.env'
)


def get_config(dotenv_path: Path = DOTENV_PATH) -> Config:
    config = dotenv_values(dotenv_path)
    return Config(
        client_id=defined(config['client_id']),
        client_secret=defined(config['client_secret']),
        access_token=defined(config['access_token']),
        api_base_url=defined(config['api_base_url']),
        server_origin=defined(config['server_origin']),
        sqlfn=defined(config['sqlfn']),
    )
