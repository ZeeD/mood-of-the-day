from typing import TypedDict

from dotenv import dotenv_values


class Config(TypedDict):
    client_id: str
    client_secret: str
    access_token: str
    api_base_url: str
    server_origin: str


def defined(value: str | None) -> str:
    assert value is not None
    return value


def get_config() -> Config:
    config = dotenv_values()
    return Config(
        client_id=defined(config['client_id']),
        client_secret=defined(config['client_secret']),
        access_token=defined(config['access_token']),
        api_base_url=defined(config['api_base_url']),
        server_origin=defined(config['server_origin']),
    )
