import logging
import os
import subprocess
import tempfile
import time
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200MB


def get_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    ip = get_ip()

    if "file" not in request.files:
        app.logger.warning("%s - no file in request", ip)
        return "No file uploaded", 400

    file = request.files["file"]
    filename = secure_filename(file.filename)

    if not filename.endswith(".ipynb"):
        app.logger.warning("%s - rejected file: %s", ip, file.filename)
        return "File must be a .ipynb notebook", 400

    app.logger.info("%s - converting: %s", ip, filename)
    start = time.monotonic()

    with tempfile.TemporaryDirectory() as tmpdir:
        notebook_path = os.path.join(tmpdir, filename)
        file.save(notebook_path)

        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nbconvert_templates")
        result = subprocess.run(
            [
                "jupyter", "nbconvert", "--to", "webpdf",
                "--template", "webpdf-linebreak",
                f"--TemplateExporter.extra_template_basedirs={template_dir}",
                notebook_path,
            ],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )

        elapsed = time.monotonic() - start

        if result.returncode != 0:
            app.logger.error("%s - conversion failed: %s (%.1fs)\n%s", ip, filename, elapsed, result.stderr)
            return "Conversion failed. The server logs may have more details.", 500

        pdf_name = filename.rsplit(".", 1)[0] + ".pdf"
        pdf_path = os.path.join(tmpdir, pdf_name)

        if not os.path.exists(pdf_path):
            app.logger.error("%s - PDF not generated: %s (%.1fs)", ip, filename, elapsed)
            return "PDF not generated", 500

        app.logger.info("%s - done: %s (%.1fs)", ip, filename, elapsed)
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_name,
            mimetype="application/pdf",
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
