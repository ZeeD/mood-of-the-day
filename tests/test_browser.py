from unittest import TestCase

from moodoftheday.browser import get_youtube_url


class TestBrowser(TestCase):
    def test_get_youtube_url(self) -> None:
        artist = 'rem'
        title = 'man on the moon'

        actual = get_youtube_url(artist, title)
        self.assertEqual('https://www.youtube.com/watch?v=dLxpNiF0YKs', actual)
