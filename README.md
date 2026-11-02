# repoclock

A small Python server that serves stuff as SVG.

## Run

    python3 server.py

Open http://localhost:8000

## Clock

Shows UTC time as big digits. Refreshes every second.

Put it in a page:

    <img src="http://localhost:8000/api/clock" alt="clock">

## Intro repo readme

Put your github username and it'll show your `username/username` repo readme as an svg. Updates every second.

Put it in a page:

    <img src="http://localhost:8000/api/intro?user=YOURUSERNAME" alt="intro">

## Files

server.py is the whole thing. README.md is this file.
