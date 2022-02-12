import os
import tempfile
from os import listdir
from os.path import isfile

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

import converter
import utils
from converter import file_allowed, allowed_file_types

app = Flask(__name__)
upload_dir = "./out"
app.config["UPLOAD_FOLDER"] = upload_dir
generated_path = tempfile.mkdtemp()


@app.route("/", methods=["GET"])
def index():
    all_files = [
        f
        for f in listdir(app.config["UPLOAD_FOLDER"])
        if isfile(os.path.join(app.config["UPLOAD_FOLDER"], f))
    ]
    return render_template("index.html", files=all_files)


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")


@app.route("/datasets", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return utils.create_error_page("Need a file")
    file = request.files["file"]
    if file == "":
        return utils.create_error_page("Need a file")

    if file and file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("index"))
    else:
        return utils.create_error_page(
            f"File is only allowed to be of the following types: {', '.join(allowed_file_types)}"
        )


@app.route("/export/<filename>", methods=["POST"])
def download_file(filename: str):
    if not converter.file_exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
        return utils.create_error_page(f"File is not available")

    filetype = request.form["filetype"]
    if filetype not in converter.allowed_file_types:
        return utils.create_error_page("Filetype is not allowed")
    try:
        converted_file = converter.convert_file(
            os.path.join(app.config["UPLOAD_FOLDER"], filename),
            generated_path,
            filetype,
        )
        return send_from_directory(generated_path, converted_file)
    except ValueError:
        return utils.create_error_page("Cannot convert file")


if __name__ == "__main__":
    app.run()
