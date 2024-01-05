from urllib.parse import parse_qs
from urllib.parse import quote_plus
from urllib.parse import urlsplit
from urllib.parse import urlunsplit

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait


def get_youtube_url(artist: str, title: str) -> str:
    search_query = quote_plus(f'{artist} {title}')
    url = f'https://www.youtube.com/results?search_query={search_query}'

    driver = webdriver.Firefox()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout=10)
        wait.until(
            presence_of_element_located((By.CSS_SELECTOR, 'a#video-title'))
        )
        href = driver.find_element(
            By.CSS_SELECTOR, 'a#video-title'
        ).get_attribute('href')
        if href is None:
            raise SystemExit(-1)
        # only keep v=...
        scheme, netloc, path, query_old, fragment = urlsplit(href)
        query_new = f'v={quote_plus(parse_qs(query_old)["v"][0])}'
        return urlunsplit((scheme, netloc, path, query_new, fragment))
    finally:
        driver.quit()
