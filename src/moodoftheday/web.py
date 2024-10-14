from html import escape
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from io import BufferedIOBase
from json import dumps
from json import loads
from logging import exception
from logging import info
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import cast
from urllib.request import Request
from urllib.request import urlopen
from webbrowser import open

from moodoftheday.browser import get_youtube_url

if TYPE_CHECKING:
    from datetime import datetime

    from moodoftheday.config import Config
    from moodoftheday.db import Db

HTML = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="icon" href="data:;base64,=" />
        <title>mood of the day</title>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>id</th>
                    <th>artist</th>
                    <th>title</th>
                    <th>youtube_url</th>
                    <th>creation_date</th>
                    <th>published_date</th>
                </tr>
            </thead>
            <tbody>
%s
            </tbody>
        </table>
    </body>
</html>
"""


def html(row: tuple[int, str, str, str, 'datetime', 'datetime']) -> str:
    (id_, artist, title, youtube_url, creation_date, published_date) = row
    return f"""<tr>
        <td>{id_}</td>
        <td>{escape(artist)}</td>
        <td>{escape(title)}</td>
        <td><a href="{escape(youtube_url)}">{escape(youtube_url)}</a></td>
        <td>{creation_date}</td>
        <td>{published_date}</td>
    </tr>"""


def request_handler(db: 'Db') -> type[BaseHTTPRequestHandler]:
    def read(rfile: BufferedIOBase, size: int = 1024) -> str:
        chunks: bytes = b''
        while True:
            chunk = rfile.read1(size)
            chunks += chunk
            if len(chunk) < size:
                break
        return chunks.decode()

    class RequestHandler(BaseHTTPRequestHandler):
        db: ClassVar['Db']

        def do_GET(self) -> None:  # noqa: N802
            self.log_message('GET')
            self.log_request(200)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                HTML.replace(
                    '%s', '\n'.join(html(row) for row in self.db.all_rows())
                ).encode()
            )
            self.wfile.flush()

        def do_POST(self) -> None:  # noqa: N802
            self.log_message('POST')
            try:
                data = loads(read(cast(BufferedIOBase, self.rfile)))
                artist = data['artist']
                title = data['title']
                youtube_url = data['youtube_url']
                id_ = self.db.append(artist, title, youtube_url)
            except:  # noqa: E722
                exception('POST')
                self.send_error(400)
                self.end_headers()
                self.wfile.write(dumps({'error': ''}).encode())
                self.wfile.flush()
            else:
                self.log_request(200)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(dumps({'id': id_}).encode())
                self.wfile.flush()

    RequestHandler.db = db
    return RequestHandler


def serve_webui(db: 'Db', *, open_browser: bool = False) -> None:
    httpd = ThreadingHTTPServer(('', 8000), request_handler(db))
    if open_browser:
        open('localhost:8000')
    httpd.serve_forever()


def client_append(config: 'Config', artist: str, title: str) -> None:
    response = urlopen(  # noqa: S310
        Request(  # noqa: S310
            config['server_origin'],
            data=dumps(
                {
                    'artist': artist.title(),
                    'title': title.capitalize(),
                    'youtube_url': get_youtube_url(artist, title),
                }
            ).encode(),
            method='POST',
        )
    )
    info('response: %s %s', response.status, response.reason)
    info('response: %s', response.read())
