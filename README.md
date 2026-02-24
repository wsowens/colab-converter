# Jupyter to PDF

A simple web app to convert Jupyter notebooks to PDF.

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
