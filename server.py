import http.server
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs
import urllib.request

PORT = 8000

DIGITS = {
    "0": (" _ ", "| |", "|_|"),
    "1": ("   ", "  |", "  |"),
    "2": (" _ ", " _|", "|_ "),
    "3": (" _ ", " _|", " _|"),
    "4": ("   ", "|_|", "  |"),
    "5": (" _ ", "|_ ", " _|"),
    "6": (" _ ", "|_ ", "|_|"),
    "7": (" _ ", "  |", "  |"),
    "8": (" _ ", "|_|", "|_|"),
    "9": (" _ ", "|_|", " _|"),
    ":": (" . ", "   ", " . "),
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>repoclock</title>
<style>
html, body { margin: 0; background: #000000; color: #ffffff; font-family: Courier New, monospace; }
body { display: flex; flex-direction: column; align-items: center; gap: 20px; padding: 40px; }
img { max-width: 90vw; }
form { display: flex; gap: 10px; }
input { background: #111; color: #fff; border: 1px solid #333; padding: 6px 10px; font-family: Courier New, monospace; }
button { background: #222; color: #fff; border: 1px solid #444; padding: 6px 10px; }
a { color: #aaa; }
</style>
</head>
<body>
<h2>repoclock</h2>
<img id="clock" src="/api/clock" alt="clock">

<form action="/" method="get">
  <input name="user" placeholder="github username" autocomplete="off">
  <button>show intro repo</button>
</form>

<div id="intro"></div>

<script>
setInterval(function () {
  document.getElementById("clock").src = "/api/clock?" + Date.now();
  var introImg = document.getElementById("introImg");
  if (introImg) {
    introImg.src = introImg.dataset.base + "?" + Date.now();
  }
}, 1000);
</script>
</body>
</html>
"""


def clock_svg():
    now = datetime.now(timezone.utc)
    rows = ["", "", ""]
    for char in now.strftime("%H:%M:%S"):
        glyph = DIGITS[char]
        for row in range(3):
            rows[row] += glyph[row]
    lines = "".join(
        f'<tspan x="200" dy="{0 if row == 0 else 30}">{text}</tspan>'
        for row, text in enumerate(rows)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="140" viewBox="0 0 400 140">
  <rect width="400" height="140" fill="#000000"/>
  <text x="200" y="45" fill="#ffffff" font-family="Courier New, monospace" font-size="24" text-anchor="middle" xml:space="preserve">{lines}</text>
</svg>"""


def intro_svg(user):
    text = ""
    try:
        url = "https://raw.githubusercontent.com/%s/%s/main/README.md" % (user, user)
        req = urllib.request.Request(url, headers={"User-Agent": "repoclock"})
        with urllib.request.urlopen(req, timeout=3) as r:
            raw = r.read(4000)
        text = raw.decode("utf-8", errors="ignore")
    except Exception as e:
        text = "could not load %s/%s/README.md" % (user, user)

    lines = []
    for line in text.splitlines():
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if len(line) > 90:
            line = line[:87] + "..."
        lines.append(line)

    if not lines:
        lines = ["empty readme?"]

    tsps = []
    for i, l in enumerate(lines[:40]):
        dy = 18 if i > 0 else 0
        tsps.append(f'<tspan x="20" dy="{dy}">{l}</tspan>')

    h = 40 + len(lines[:40]) * 18
    if h < 120:
        h = 120

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="700" height="{h}">
  <rect width="700" height="{h}" fill="#0d1117"/>
  <text x="20" y="30" fill="#c9d1d9" font-family="Courier New, monospace" font-size="14" xml:space="preserve">{''.join(tsps)}</text>
</svg>"""


class ClockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            user = qs.get("user", [""])[0].strip()
            page = PAGE
            if user:
                img = '<p>your intro repo</p><img id="introImg" data-base="/api/intro?user=%s" src="/api/intro?user=%s" alt="intro"></p><a href="/">back</a>' % (user, user)
                page = page.replace('<div id="intro"></div>', '<div id="intro">%s</div>' % img)
            self.send_body(page.encode("utf-8"), "text/html; charset=utf-8")
        elif path.startswith("/api/clock"):
            self.send_body(clock_svg().encode("utf-8"), "image/svg+xml; charset=utf-8")
        elif path.startswith("/api/intro"):
            user = qs.get("user", [""])[0].strip()
            if not user or "/" in user or "\\" in user:
                self.send_error(400)
                return
            self.send_body(intro_svg(user).encode("utf-8"), "image/svg+xml; charset=utf-8")
        else:
            self.send_error(404)

    def send_body(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), ClockHandler) as httpd:
        print(f"Clock running at http://localhost:{PORT}")
        httpd.serve_forever()
