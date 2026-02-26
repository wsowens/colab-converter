# Colab Converter

A simple web app to convert Jupyter notebooks to PDFs. We're essentially just wrapping a terminal command with a Flask app:

> jupyter nbconvert --to pdf {$FILENAME}

This app is 95% written by Claude, use at your own risk.

## Installation

**1. System dependencies (Ubuntu)**

```bash
apt install texlive-xetex texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra pandoc
```

**2. Python dependencies**

```bash
pip install -r requirements.txt
```



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
