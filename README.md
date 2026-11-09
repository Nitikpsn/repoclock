# repoclock

repoclock is a small python server. it draws a clock, a year progress bar, and
a github readme as svg images. no packages, no build step.

![repoclock demo](docs/preview.png)

## live clock

this image comes from my pythonanywhere app. github asks the server for it when
the page loads, so it shows the current time.

![clock](https://nitikpsn.pythonanywhere.com/api/clock?bg=0d1117&fg=c9d1d9)

![year progress](https://nitikpsn.pythonanywhere.com/api/progress?of=year)

## run it on localhost

you need python 3.9 or newer. nothing else.

    python3 server.py

open http://localhost:8000

## what it does

- `/api/clock` makes the clock
- `/api/progress` makes the progress bar
- `/api/intro?user=YOURNAME` makes the readme image

put those links in your own readme if you want.

## AND more

- [how to use it](docs/usage.md)
- [deploy on pythonanywhere](docs/deploy-pythonanywhere.md)
