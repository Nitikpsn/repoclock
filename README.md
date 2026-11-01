# repoclock

A small Python server that serves an ASCII clock as an SVG.

## Run

    python3 server.py

Open http://localhost:8000 to see it tick.

## Put it in a page

    <img src="http://localhost:8000/api/clock" alt="clock">

The clock uses UTC time and redraws on every request. White digits, black background.

## Files

server.py is the whole thing. README.md is this file.
