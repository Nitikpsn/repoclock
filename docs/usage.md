# how to use repoclock

repoclock makes svg images you can put in a github readme. there are three:

- a clock
- a progress bar for the year, month, week, or day
- your github profile readme as plain text

## use the one i host

the easy way is to use my pythonanywhere site:

    https://nitikpsn.pythonanywhere.com

put this in your readme:

    <img src="https://nitikpsn.pythonanywhere.com/api/clock?bg=none&fg=c9d1d9" alt="clock">

use `https`, not `http`. github will not load http images.

progress bar:

    <img src="https://nitikpsn.pythonanywhere.com/api/progress?of=year" alt="year progress">

if you want to run it yourself, see [run your own](#run-your-own). then just
change the domain in these links.

## run your own

you need python 3.9 or newer. nothing to install.

    python3 server.py

open http://localhost:8000. press ctrl+c to stop it.

## clock

the clock uses utc by default. to show another timezone, add `tz`:

    <img src="https://nitikpsn.pythonanywhere.com/api/clock?tz=Asia/Kolkata" alt="clock">

other options:

- `bg` background color. default `000000`. use `none` for transparent.
- `fg` text color. default `ffffff`.
- `seconds` set to `0` to hide seconds.
- `hour12` set to `1` for a 12 hour clock.

if you use `bg=none`, change `fg` too. white text on a white page is invisible.

## progress bar

`of` can be `year`, `month`, `week`, or `day`. default is `year`.

    <img src="https://nitikpsn.pythonanywhere.com/api/progress?of=month&bg=none&bar=58a6ff" alt="month progress">

`bar` is the color of the filled part. `bg` and `fg` work like the clock.

## readme image

this only works if you have a repo named the same as your username. github shows
that repo on your profile.

    <img src="https://nitikpsn.pythonanywhere.com/api/intro?user=YOURNAME" alt="intro">

it takes the first 40 lines and removes links, images, html tags, and badges.
`bg` and `fg` work here too.

if it does not update, add something like `&v=2` to the url.
