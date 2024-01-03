from unittest import TestCase

from moodoftheday.mastoclient import get_config_from_dotenv


class TestMastoclient(TestCase):
    def test_get_config_from_dotenv(self) -> None:
        config = get_config_from_dotenv()
        self.assertIsNotNone(config['client_id'])
        self.assertIsNotNone(config['client_secret'])
        self.assertIsNotNone(config['access_token'])
        self.assertIsNotNone(config['api_base_url'])
