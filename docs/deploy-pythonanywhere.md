# put repoclock online

this is for pythonanywhere. it has a free plan and can run this app.

pythonanywhere does not run `python3 server.py`. it runs wsgi apps, so the repo
has `wsgi.py`.

## 1. get the code there

make a free account at <https://www.pythonanywhere.com>.

open a bash console and clone the repo:

    git clone https://github.com/Nitikpsn/repoclock.git

if you forked it, use your own repo url. if your repo is private, upload a zip
from the Files tab and unzip it to `~/repoclock`.

## 2. make the web app

1. open the Web tab
2. click Add a new web app
3. keep your free domain
4. pick Manual configuration, not Flask
5. pick Python 3.10 or newer

## 3. fill the settings

- Source code: `/home/YOURNAME/repoclock`
- Working directory: `/home/YOURNAME/repoclock`
- Virtualenv: leave it empty

now click the WSGI configuration file link and replace everything with:

```python
import sys

path = "/home/YOURNAME/repoclock"
if path not in sys.path:
    sys.path.insert(0, path)

from wsgi import application
```

change `YOURNAME` to your username and save.

## 4. reload and check

click Reload on the Web tab. then open:

    https://YOURNAME.pythonanywhere.com

you should see the clock and the progress bar. the code boxes at the bottom of
the page will show your own domain. copy one into your github readme.

## update it later

push your changes, then run this on pythonanywhere:

    cd ~/repoclock
    git pull

click Reload again. the site keeps the old code until you do.

## if it breaks

- 502 or 504: open Web > Log files > Error log. most of the time the path or
  username is wrong.
- `ModuleNotFoundError: No module named 'wsgi'`: check the path in the WSGI
  file. also make sure `wsgi.py` was pushed.
- every page is 404: the WSGI file must import `application`, and you must use
  Manual configuration.
- intro says "empty readme?": the `YOURNAME/YOURNAME` repo or its readme is
  missing.
- intro image is old: wait a minute, or add `&v=2` to the image url.

## free plan stuff

- use `https` in your image links.
- free apps can be disabled if nobody opens them for a long time. log in and
  click Reload to wake it up.
- custom domains cost money. `YOURNAME.pythonanywhere.com` is free.
