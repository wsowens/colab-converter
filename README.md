# Jupyter to PDF

A simple web app to convert Jupyter notebooks to PDF.
This app is 95% written by Claude, use at your own risk.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

If you've definitely run `playwright install chromium` and you're still getting an error like:

> RuntimeError: No suitable chromium executable found on the system. Please
  use '--allow-chromium-download' to allow downloading one,or install it using `playwright install chromium`.

  The headless chromium installed by playwright is probably missing dynamic libraries. Try running 
  > playwright pdf "google.com" test.pdf

  Until you can get this to succeed. This is a list of packages I had to install in order to get things working. 



## Running

**Development:**
```bash
python app.py
```

**Production:**
```bash
gunicorn app:app
```

Then open http://localhost:8000 (gunicorn) or http://localhost:5000 (dev).

required packages (because for some reason headless chromium doesn't come with everything)

> apt install libatk1.0-dev libatk1.0-0t64 libatk-bridge2.0-dev libxcomposite1 libxcomposite-dev libxdamage-dev libxrandr-dev libasound-dev