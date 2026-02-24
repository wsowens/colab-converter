import os
import subprocess
import tempfile
from flask import Flask, request, send_file, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if not file.filename.endswith(".ipynb"):
        return "File must be a .ipynb notebook", 400

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded notebook
        notebook_path = os.path.join(tmpdir, file.filename)
        file.save(notebook_path)

        # Convert to PDF
        result = subprocess.run(
            ["jupyter", "nbconvert", "--to", "webpdf", notebook_path],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )

        if result.returncode != 0:
            return f"Conversion failed: {result.stderr}", 500

        # Find the PDF
        pdf_name = file.filename.rsplit(".", 1)[0] + ".pdf"
        pdf_path = os.path.join(tmpdir, pdf_name)

        if not os.path.exists(pdf_path):
            return "PDF not generated", 500

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_name,
            mimetype="application/pdf",
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
