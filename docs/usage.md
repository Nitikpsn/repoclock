# how to use repoclock

repoclock is a small python server. it returns svg images: a clock, a progress
bar, and a text version of a github readme.

## run it on localhost

you need python 3.9 or newer. there is nothing to install.

    python3 server.py

open http://localhost:8000. press ctrl+c in the terminal to stop it.

## clock

    http://localhost:8000/api/clock

it uses the time on the server. these query params change how it looks:

| param   | default | what it does                           |
| ------- | ------- | -------------------------------------- |
| tz      | UTC     | timezone, like `Asia/Kolkata`          |
| bg      | 000000  | hex color, or `none` for no background |
| fg      | ffffff  | text color                             |
| seconds | 1       | `0` hides the seconds                  |
| hour12  | 0       | `1` for a 12 hour clock                |

example:

    <img src="http://localhost:8000/api/clock?tz=Asia/Kolkata" alt="clock">

if you use `bg=none`, the clock has no background. then you should change `fg`
so it can be seen on your page.

## progress bar

    http://localhost:8000/api/progress

it shows how much of the year is gone. the `of` param can be `year`, `month`,
`week`, or `day`.

    <img src="http://localhost:8000/api/progress?of=month&bg=none&bar=58a6ff" alt="month progress">

`bg` and `fg` work the same as on the clock. `bar` is the color of the filled
part.

## readme image

    http://localhost:8000/api/intro?user=YOURNAME

this reads `YOURNAME/YOURNAME` from github and draws the first 40 lines of the
readme. links, images, html tags, and badges are removed. `bg` and `fg` work the
same as on the clock.

the readme is cached for 60 seconds. github images are cached too. if you change
your readme and still see the old one, add something like `&v=2` to the url.

## use it on github

github loads images through its own proxy. the clock sends `no-store`, so it
should ask for a new image each time. if the time still looks old, reload the
page.

use `https` in image urls. github blocks `http` images on its https pages.

the deployed app here is:

    https://nitikpsn.pythonanywhere.com

so an image for your readme looks like this:

    <img src="https://nitikpsn.pythonanywhere.com/api/clock?bg=none&fg=c9d1d9" alt="clock">

## deploy

the pythonanywhere steps are in
[deploy-pythonanywhere.md](deploy-pythonanywhere.md).
