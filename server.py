import http.server
from datetime import datetime, timezone

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
html, body { margin: 0; height: 100%; background: #000000; }
body { display: grid; place-items: center; }
img { width: 400px; height: 140px; }
</style>
</head>
<body>
<img id="clock" src="/api/clock" alt="clock">
<script>
setInterval(function () {
  document.getElementById("clock").src = "/api/clock?" + Date.now();
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


class ClockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_body(PAGE.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path.startswith("/api/clock"):
            self.send_body(clock_svg().encode("utf-8"), "image/svg+xml; charset=utf-8")
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
