# Jupyter to PDF

A simple web app to convert Jupyter notebooks to PDF.
This app is 95% written by Claude, use at your own risk.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
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
