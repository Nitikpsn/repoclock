# repoclock

A small Python server that draws a UTC clock and a GitHub readme as SVG.
No packages to install, no build step.

![repoclock demo](docs/preview.png)

## Run

    python3 server.py

Then open http://localhost:8000.

## Clock

    <img src="http://localhost:8000/api/clock" alt="clock">

It refreshes every second. Query params:

| param   | default | what it does                          |
| ------- | ------- | ------------------------------------- |
| tz      | UTC     | IANA timezone, e.g. `Asia/Kolkata`    |
| bg      | 000000  | hex color, or `none` for no background |
| fg      | ffffff  | text color                            |
| seconds | 1       | `0` hides the seconds                 |
| hour12  | 0       | `1` for a 12 hour clock               |

The no-background version:

    <img src="http://localhost:8000/api/clock?bg=none&fg=c9d1d9" alt="clock">

`bg=none` skips the background rectangle, so the clock sits on whatever
background the page already has. Change `fg` to something readable on your
theme; the default white disappears on a white page.

## Intro readme

    <img src="http://localhost:8000/api/intro?user=YOURNAME" alt="intro">

This fetches `YOURNAME/YOURNAME/README.md` from GitHub and draws the first 40
lines. Markdown links, images, HTML tags and badges are stripped so it reads
like text. `bg` and `fg` work the same as on the clock.

Intro images are cached for a minute so every page view does not hit GitHub.
The clock is never cached.

## Notes

- Python 3.9+ (the timezone support comes from `zoneinfo`).
- Unknown timezones quietly fall back to UTC.
- The username is checked against GitHub's rules before it goes into a URL.
- GitHub proxies README images and caches them. If you change the README and
  still see the old one, wait a bit or bump a version in the URL, like
  `?user=YOURNAME&v=2`.

`server.py` is the whole server.
