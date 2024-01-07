from datetime import datetime
from html import escape
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from typing import ClassVar
from webbrowser import open

from .db import Db

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


def html(row: tuple[int, str, str, str, datetime, datetime]) -> str:
    (id_, artist, title, youtube_url, creation_date, published_date) = row
    return f"""\
                <tr>
                    <td>{id_}</td>
                    <td>{escape(artist)}</td>
                    <td>{escape(title)}</td>
                    <td><a href="{escape(youtube_url)}">{escape(youtube_url)}</a></td>
                    <td>{creation_date}</td>
                    <td>{published_date}</td>
                </tr>"""


def request_handler(db: Db) -> type[BaseHTTPRequestHandler]:
    class RequestHandler(BaseHTTPRequestHandler):
        db: ClassVar[Db]

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

    RequestHandler.db = db
    return RequestHandler


def serve_webui(db: Db, *, open_browser: bool = False) -> None:
    httpd = ThreadingHTTPServer(('', 8000), request_handler(db))
    if open_browser:
        open('localhost:8000')
    httpd.serve_forever()
