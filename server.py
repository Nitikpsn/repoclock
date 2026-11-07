import html
import http.server
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python 3.8 and older
    ZoneInfo = None

PORT = 8000

USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
HEX_RE = re.compile(r"^[0-9a-fA-F]{6}$")

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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>repoclock</title>
<style>
body {
  margin: 0;
  padding: 42px 20px 60px;
  background: #0d1117;
  color: #c9d1d9;
  font-family: "Courier New", monospace;
  font-size: 14px;
}
main { max-width: 690px; margin: 0 auto; }
h1 { margin: 0 0 2px; font-size: 24px; font-weight: normal; }
p { margin: 0 0 14px; }
.sub { color: #8b949e; margin-bottom: 26px; }
img { display: block; max-width: 100%; height: auto; }
img + img { margin-top: 10px; }
form { display: flex; gap: 6px; flex-wrap: wrap; margin: 26px 0 10px; }
input, button {
  font: inherit;
  padding: 5px 8px;
  background: #161b22; 
  color: #c9d1d9;
  border: 1px solid #30363d;
  border-radius: 3px;
}
button { background: #21262d; cursor: pointer; }
button:active { background: #30363d; }
a { color: #58a6ff; }
hr { border: 0; border-top: 1px solid #21262d; margin: 28px 0 12px; }
pre {
  margin: 8px 0;
  padding: 8px 10px;
  overflow-x: auto;
  background: #11161d;
  border: 1px solid #262c36;
  font-size: 12px;
  color: #9da7b3;
}
.note { color: #6e7681; font-size: 12px; margin: 26px 0 8px; }
</style>
</head>
<body>
<main>
<h1>repoclock</h1>
<p class="sub">a clock, a progress bar, and your github readme as svg.</p>

<img id="clock" src="/api/clock" alt="clock">
<img id="progress" src="/api/progress" alt="progress">

<form action="/" method="get">
  <input name="user" placeholder="github username" autocomplete="off" value="{user}">
  <button>show readme</button>
</form>

{intro}

<hr>
<p class="note">stick one of these in a readme:</p>
<pre>&lt;img src="{base}/api/clock" alt="clock"&gt;</pre>
<pre>&lt;img src="{base}/api/clock?bg=none&amp;tz=Asia/Kolkata" alt="clock"&gt;</pre>
<pre>&lt;img src="{base}/api/progress?of=year" alt="year progress"&gt;</pre>
</main>

<script>
var clock = document.getElementById("clock");
var src = clock.getAttribute("src");
setInterval(function () {
  clock.src = src + (src.indexOf("?") < 0 ? "?" : "&") + Date.now();
}, 1000);

var progress = document.getElementById("progress");
setInterval(function () {
  progress.src = "/api/progress?" + Date.now();
}, 60000);
</script>
</body>
</html>
"""


def pick_color(query, name, default):
    value = query.get(name, [default])[0].strip().lstrip("#")
    if HEX_RE.match(value):
        return "#" + value
    return "#" + default


def pick_background(query, default):
    value = query.get("bg", [default])[0].strip().lower().lstrip("#")
    if value in ("none", "transparent", "clear", "0"):
        return None
    if HEX_RE.match(value):
        return "#" + value
    return "#" + default


def clock_zone(query):
    name = query.get("tz", ["UTC"])[0].strip()
    if not name or name.upper() == "UTC" or ZoneInfo is None:
        return timezone.utc
    try:
        return ZoneInfo(name)
    except Exception:
        return timezone.utc


def clock_svg(query):
    now = datetime.now(clock_zone(query))
    show_seconds = query.get("seconds", ["1"])[0].lower() not in ("0", "false", "no")
    hour12 = query.get("hour12", ["0"])[0].lower() in ("1", "true", "yes")

    if hour12:
        stamp = now.strftime("%I:%M:%S" if show_seconds else "%I:%M")
        if stamp.startswith("0"):
            stamp = stamp[1:]
    else:
        stamp = now.strftime("%H:%M:%S" if show_seconds else "%H:%M")

    rows = ["", "", ""]
    for char in stamp:
        glyph = DIGITS[char]
        for row in range(3):
            rows[row] += glyph[row]

    # Courier New is 0.6 em wide, so this leaves a small margin either side.
    width = int(len(stamp) * 3 * 24 * 0.6) + 40
    height = 140
    background = pick_background(query, "000000")
    foreground = pick_color(query, "fg", "ffffff")

    lines = "".join(
        f'<tspan x="{width // 2}" dy="{0 if row == 0 else 30}">{text}</tspan>'
        for row, text in enumerate(rows)
    )
    rect = f'<rect width="{width}" height="{height}" fill="{background}"/>' if background else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {rect}
  <text x="{width // 2}" y="45" fill="{foreground}" font-family="Courier New, monospace" font-size="24" text-anchor="middle" xml:space="preserve">{lines}</text>
</svg>"""


def progress_svg(query):
    now = datetime.now(clock_zone(query))
    kind = query.get("of", ["year"])[0].lower()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if kind == "day":
        begin = start
        end = begin + timedelta(days=1)
        label = begin.strftime("%a, %b %d")
    elif kind == "week":
        begin = start - timedelta(days=start.weekday())
        end = begin + timedelta(days=7)
        label = "week of " + begin.strftime("%b %d")
    elif kind == "month":
        begin = start.replace(day=1)
        end = (begin + timedelta(days=32)).replace(day=1)
        label = begin.strftime("%B %Y")
    else:
        begin = start.replace(month=1, day=1)
        end = begin.replace(year=begin.year + 1)
        label = begin.strftime("%Y")

    total = (end - begin).total_seconds()
    pct = (now - begin).total_seconds() / total * 100
    pct = max(0.0, min(100.0, pct))

    width = 460
    height = 96
    bar_x = 20
    bar_y = 54
    bar_w = width - bar_x * 2
    bar_h = 14
    fill_w = bar_w * pct / 100

    background = pick_background(query, "0d1117")
    foreground = pick_color(query, "fg", "c9d1d9")
    bar = pick_color(query, "bar", "3fb950")
    rect = f'<rect width="{width}" height="{height}" fill="{background}"/>' if background else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {rect}
  <text x="20" y="30" fill="{foreground}" font-family="Courier New, monospace" font-size="14">{label}</text>
  <text x="440" y="30" fill="{foreground}" font-family="Courier New, monospace" font-size="14" text-anchor="end">{pct:.1f}%</text>
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" fill="#30363d"/>
  <rect x="{bar_x}" y="{bar_y}" width="{fill_w:.1f}" height="{bar_h}" rx="7" fill="{bar}"/>
</svg>"""


def read_github_readme(user):
    for name in ("README.md", "README"):
        url = f"https://raw.githubusercontent.com/{user}/{user}/HEAD/{name}"
        request = urllib.request.Request(url, headers={"User-Agent": "repoclock"})
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                return response.read(8000).decode("utf-8", errors="ignore")
        except Exception:
            continue
    return ""


def clean_markdown(line):
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)  # drop images and badges
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)  # keep link text
    line = re.sub(r"<[^>]+>", "", line)
    line = html.unescape(line)
    line = re.sub(r"^#{1,6}\s*", "", line)
    line = re.sub(r"^>\s?", "", line)
    line = re.sub(r"^\s*[-*+]\s+", "- ", line)
    line = re.sub(r"(\*\*|__|`)", "", line)
    return line.strip()


def intro_svg(user, query):
    text = read_github_readme(user)
    lines = []
    for raw in text.splitlines():
        line = clean_markdown(raw)
        if line:
            lines.append(line)
        elif lines and lines[-1] != "":
            lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    lines = [line[:78] for line in lines[:40]]
    if not lines:
        lines = ["empty readme?"]

    height = max(120, 40 + len(lines) * 18)
    background = pick_background(query, "0d1117")
    foreground = pick_color(query, "fg", "c9d1d9")

    tspans = []
    for i, line in enumerate(lines):
        tspans.append(f'<tspan x="20" dy="{18 if i > 0 else 0}">{html.escape(line, quote=False)}</tspan>')
    rect = f'<rect width="720" height="{height}" fill="{background}"/>' if background else ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}">
  {rect}
  <text x="20" y="30" fill="{foreground}" font-family="Courier New, monospace" font-size="14" xml:space="preserve">{''.join(tspans)}</text>
</svg>"""


def page(user):
    shown = html.escape(user)
    intro = ""
    if user:
        if USERNAME_RE.match(user):
            intro = (
                '<p>readme from <a href="https://github.com/%s">@%s</a></p>\n'
                '<img src="/api/intro?user=%s" alt="%s readme">'
                % (shown, shown, shown, shown)
            )
        else:
            intro = "<p>that does not look like a github username.</p>"
    return PAGE.replace("{user}", shown).replace("{intro}", intro)


class ClockHandler(http.server.BaseHTTPRequestHandler):
    server_version = "repoclock/1.0"

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/":
            user = query.get("user", [""])[0].strip()
            self.send_body(page(user).encode("utf-8"), "text/html; charset=utf-8")
        elif parsed.path == "/api/clock":
            self.send_body(clock_svg(query).encode("utf-8"), "image/svg+xml; charset=utf-8")
        elif parsed.path == "/api/progress":
            svg = progress_svg(query)
            self.send_body(
                svg.encode("utf-8"),
                "image/svg+xml; charset=utf-8",
                "public, max-age=30",
            )
        elif parsed.path == "/api/intro":
            user = query.get("user", [""])[0].strip()
            if not USERNAME_RE.match(user):
                self.send_error(400, "bad username")
                return
            svg = intro_svg(user, query)
            self.send_body(
                svg.encode("utf-8"),
                "image/svg+xml; charset=utf-8",
                "public, max-age=60",
            )
        else:
            self.send_error(404)

    def send_body(self, body, content_type, cache="no-store"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", cache)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), ClockHandler) as httpd:
        print(f"repoclock running at http://localhost:{PORT}")
        httpd.serve_forever()
