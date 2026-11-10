# repoclock

your readme, but it can tell time.

repoclock is a tiny python server that makes live svg images for your github
profile. clock, progress bar, profile readme. no packages, no build step.

![repoclock demo](docs/preview.png)

## live

![clock](https://nitikpsn.pythonanywhere.com/api/clock?bg=0d1117&fg=c9d1d9)

![year progress](https://nitikpsn.pythonanywhere.com/api/progress?of=year)

## what you get

- a clock for any timezone. 12 or 24 hour, seconds on or off
- a progress bar for the year, month, week, or day
- your github readme as a text image, badges removed
- transparent mode and custom colors
- one python file, no packages

## use it

copy this. keep `https`.

    <img src="https://nitikpsn.pythonanywhere.com/api/clock?bg=none&fg=c9d1d9" alt="clock">

    <img src="https://nitikpsn.pythonanywhere.com/api/progress?of=year" alt="year progress">

the profile one needs a repo named after your username:

    <img src="https://nitikpsn.pythonanywhere.com/api/intro?user=YOURNAME" alt="intro">

more options: [usage.md](docs/usage.md).

## run it

    python3 server.py

python 3.9+. open http://localhost:8000. host it free on pythonanywhere with
[these steps](docs/deploy-pythonanywhere.md).

## problems i hit

- pythonanywhere only runs wsgi apps. that is why `wsgi.py` exists.
- the deployed page had localhost links until i built the base url from the request.
- github caches images. add `&v=2` when the readme image looks old.
- the intro image needs `YOURNAME/YOURNAME` to exist.
- the free pythonanywhere app can go idle. log in and click Reload.
- use `https`. github will not load `http` images.

>>NOTE:
>>i used gemnai to help error fix i tested it, fixed what broke, and kept what worked. the ai does
>>not run when the server runs, and there is no ai api call at runtime.
>>that's it.
