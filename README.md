# Colab Converter

A simple web app to convert Jupyter notebooks to PDFs. We're essentially just wrapping a terminal command with a Flask app:

> jupyter nbconvert --to="webpdf" {$FILENAME}

This app is 95% written by Claude, use at your own risk.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

If you've definitely run `playwright install chromium` and you're still getting an error like:

> RuntimeError: No suitable chromium executable found on the system. Please
  use '--allow-chromium-download' to allow downloading one,or install it using `playwright install chromium`.

The headless chromium installed by playwright is probably missing dynamic libraries. Try running:
  > playwright pdf "google.com" test.pdf

...until it succeeds.  This is a list of packages I had to install in order to get things working:

> apt install libatk1.0-dev libatk1.0-0t64 libatk-bridge2.0-dev libxcomposite1 libxcomposite-dev libxdamage-dev libxrandr-dev libasound-dev



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

## Running as a systemd service

Edit `colab-converter.service` and replace `YOURUSER` and the two paths:

```ini
User=youruser
WorkingDirectory=/path/to/colab-converter
ExecStart=/path/to/venv/bin/gunicorn app:app
```

Then install and start it:

```bash
sudo cp colab-converter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable colab-converter
sudo systemctl start colab-converter
```

Check status and logs:

```bash
systemctl status colab-converter
journalctl -u colab-converter -f
```
