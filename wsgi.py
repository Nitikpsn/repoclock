"""Lets repoclock run on PythonAnywhere.

server.py works on its own with python3 server.py. PythonAnywhere only runs
WSGI apps, so this file gives it an application object and uses the same
helpers from server.py. Local use stays the same.
"""

import sys
from pathlib import Path
from urllib.parse import parse_qs

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from server import USERNAME_RE, clock_svg, intro_svg, page, progress_svg


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO") or "/"
    query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)

    scheme = environ.get("wsgi.url_scheme", "http")
    host = environ.get("HTTP_HOST") or environ.get("SERVER_NAME", "localhost")
    base = f"{scheme}://{host}"

    user = query.get("user", [""])[0].strip()
    cache = "no-store"
    content_type = "text/plain; charset=utf-8"

    if method not in ("GET", "HEAD"):
        status = "405 Method Not Allowed"
        body = b"method not allowed\n"
    elif path == "/":
        status = "200 OK"
        content_type = "text/html; charset=utf-8"
        body = page(user, base).encode("utf-8")
    elif path == "/api/clock":
        status = "200 OK"
        content_type = "image/svg+xml; charset=utf-8"
        body = clock_svg(query).encode("utf-8")
    elif path == "/api/progress":
        status = "200 OK"
        content_type = "image/svg+xml; charset=utf-8"
        cache = "public, max-age=30"
        body = progress_svg(query).encode("utf-8")
    elif path == "/api/intro":
        if not USERNAME_RE.match(user):
            status = "400 Bad Request"
            body = b"bad username\n"
        else:
            status = "200 OK"
            content_type = "image/svg+xml; charset=utf-8"
            cache = "public, max-age=60"
            body = intro_svg(user, query).encode("utf-8")
    else:
        status = "404 Not Found"
        body = b"not found\n"

    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
        ("Cache-Control", cache),
        ("X-Content-Type-Options", "nosniff"),
    ]
    start_response(status, headers)

    if method == "HEAD":
        return [b""]
    return [body]
