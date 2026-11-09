# Putting repoclock on PythonAnywhere

PythonAnywhere does not run `python3 server.py` for free web apps. It only runs
WSGI apps. So this repo has `wsgi.py`. It gives PythonAnywhere an `application`
object and uses the same helpers as `server.py`. You can still run the site on
your laptop with `python3 server.py` like before.

You do not need to install anything. The app only uses the Python standard
library.

## 1. Push the code

Run this in the project folder:
```bash
git add server.py wsgi.py docs/deploy-pythonanywhere.md docs/usage.md README.md
git commit -m "Add PythonAnywhere setup"
git push
```

The repo used below is `https://github.com/Nitikpsn/repoclock.git`. If your repo
is private, upload a zip from the Files tab instead. Step 3 shows how.

## 2. Make an account

Go to <https://www.pythonanywhere.com/> and sign up for the free Beginner plan.

The free plan gives you:

- one web app at `https://YOURNAME.pythonanywhere.com`
- one worker
- 512 MB of disk space
- Python 3.10 to 3.13

## 3. Get the code on the site

Open Console, then Bash. Run:

```bash
git clone https://github.com/Nitikpsn/repoclock.git
```

If the folder is already there, run this instead:

```bash
cd ~/repoclock
git pull
```

The code will be in `/home/YOURNAME/repoclock`.
If the repo is private, open the Files tab, upload a zip of the project, then
unzip it in Bash with `unzip repoclock.zip`.

## 4. Make the web app

1. Open the Web tab.
2. Click Add a new web app.
3. Keep `YOURNAME.pythonanywhere.com`.
4. Pick Manual configuration. Do not pick Flask.
5. Pick Python 3.13. Anything from 3.10 up will work.

## 5. Connect the code

Fill these in on the web app page:

- Source code: `/home/YOURNAME/repoclock`
- Working directory: `/home/YOURNAME/repoclock`
- Virtualenv: leave it empty

Now click the WSGI configuration file link. It is in the Code section. Delete
what is inside and paste this:

```python
import sys

path = "/home/YOURNAME/repoclock"
if path not in sys.path:
    sys.path.insert(0, path)

from wsgi import application
```

Change `YOURNAME` to your username and save the file.

The `sys.path.insert(0, path)` line is important. It makes Python load the
`wsgi.py` from this folder first.

## 6. Reload and check

Click Reload at the top of the Web page. Then open:

```
https://YOURNAME.pythonanywhere.com
```

You should see the clock and the progress bar. You can also test these links:

- `https://YOURNAME.pythonanywhere.com/api/clock`
- `https://YOURNAME.pythonanywhere.com/api/progress?of=month`
- `https://YOURNAME.pythonanywhere.com/api/intro?user=YOURNAME`

The code snippets at the bottom of the page will show your real domain now. You
can copy them into your GitHub README.

## 7. Update the site

Push your changes from your laptop. Then run this in the PythonAnywhere Bash
console:

```bash
cd ~/repoclock
git pull
```

After that, click Reload on the Web tab. The site keeps the old code until you
reload.

## If something goes wrong

- 502 or 504: open Web, then Log files, then Error log. Most of the time the
  path in the WSGI file is wrong or the username has a typo.
- `ModuleNotFoundError: No module named 'wsgi'`: the path is wrong, or `wsgi.py`
  was not pushed.
- Every route gives 404: the WSGI file must import `application`, not `app`. Also
  check that you picked Manual configuration.
- The intro image says "empty readme?": GitHub returned nothing. Free
  PythonAnywhere accounts can only reach sites on their allow list, and
  `raw.githubusercontent.com` is allowed. To test it, run this in Bash:

```bash
python3 -c "import urllib.request; print(urllib.request.urlopen('https://raw.githubusercontent.com/YOURNAME/YOURNAME/HEAD/README.md').status)"
```

- The intro image is old: it is cached for 60 seconds, and GitHub caches images
  too. Add `&v=2` to the image URL.

## Free plan things to know

- Web app CPU time is not part of the 100 CPU seconds for consoles. The clock
  refresh is fine. The free plan has one worker and low bandwidth, so do not
  keep many tabs open on the demo page.
- Use `https://` in image URLs. Otherwise the browser blocks them on an HTTPS
  page.
- Custom domains and SSH cost money. `YOURNAME.pythonanywhere.com` and HTTPS are
  free.
- Free web apps expire if they sit idle for too long. The current limit is about
  one month. Log in and reload the app if it has been idle.
