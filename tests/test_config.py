from unittest import TestCase

from moodoftheday.config import get_config


class TestConfig(TestCase):
    def test_get_config(self) -> None:
        config = get_config()
        self.assertIsNotNone(config['client_id'])
        self.assertIsNotNone(config['client_secret'])
        self.assertIsNotNone(config['access_token'])
        self.assertIsNotNone(config['api_base_url'])
        self.assertIsNotNone(config['server_origin'])
