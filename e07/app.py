import os
import pathlib
import tempfile
from os import listdir
from os.path import isfile

from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
)
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
    all_files = get_all_uploaded_files()
    return render_template("index.html", files=all_files)


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html", error=request.args["error"])


@app.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return utils.create_error_page("Need a file")
    file = request.files["file"]
    if file == "":
        return utils.create_error_page("Need a file")

    if file and file_allowed(file.filename):
        filename = secure_filename(file.filename)

        if filename in get_all_uploaded_files():
            return utils.create_error_page("File already exists")

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("index"))
    else:
        return utils.create_error_page(
            f"File is only allowed to be of the following types: {', '.join(allowed_file_types)}"
        )


@app.route("/export/<filename>", methods=["POST"])
def download_file(filename: str):
    if not converter.file_exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
        return utils.file_does_not_exist_error()

    filetype = request.form["filetype"]
    if filetype not in converter.allowed_file_types:
        return utils.create_error_page("Filetype is not allowed")
    try:
        converted_file = converter.convert_file(
            path_of_uploaded_file(filename),
            generated_path,
            filetype,
        )
        return send_from_directory(generated_path, converted_file)
    except ValueError:
        return utils.create_error_page("Cannot convert file")


@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename: str):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()
    os.remove(target)
    return redirect(url_for("index"))


@app.route("/details/<filename>", methods=["GET"])
def details(filename: str):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()

    pf = converter.parse_file(pathlib.Path(target))
    return render_template("details.html", pf=pf)


@app.route("/delete/<filename>/column/<column>", methods=["POST"])
def delete_column(filename, column):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()
    pf = converter.parse_file(pathlib.Path(target))
    if column not in pf.df.columns:
        return utils.create_error_page("Column does not exist")
    drop_row_or_column(target, column, is_row=False)
    return redirect(f"/details/{filename}")


@app.route("/delete/<filename>/row/<int:row>", methods=["POST"])
def delete_row(filename, row):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()
    drop_row_or_column(target, row, is_row=True)
    return redirect(f"/details/{filename}")


@app.route("/edit-cell/<filename>/<int:row>/<int:column>", methods=["GET"])
def edit_cell(filename, row, column):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()

    pf = converter.parse_file(pathlib.Path(target))
    return render_template(
        "edit_cell.html",
        filename=filename,
        row=row,
        col=column,
        value=pf.df.iloc[row, column],
    )


@app.route("/edit/<filename>/<int:row>/<int:col>", methods=["POST"])
def update_cell(filename, row, col):
    target = path_of_uploaded_file(filename)
    if not converter.file_exists(target):
        return utils.file_does_not_exist_error()

    pf = converter.parse_file(pathlib.Path(target))
    pf.df.iloc[row, col] = request.form["value"]
    pf.out_path = app.config["UPLOAD_FOLDER"]
    pf.convert_file(pf.file.suffix)
    return redirect(f"/details/{filename}")


def drop_row_or_column(target: str, idx, is_row: bool = True):
    pf = converter.parse_file(pathlib.Path(target))
    if is_row:
        pf.df.drop([idx], inplace=True)
    else:
        pf.df = pf.df.drop(columns=[idx])
    pf.out_path = app.config["UPLOAD_FOLDER"]
    pf.convert_file(pf.file.suffix)


def path_of_uploaded_file(filename: str):
    return os.path.join(app.config["UPLOAD_FOLDER"], filename)


def get_all_uploaded_files() -> list:
    return [
        f
        for f in listdir(app.config["UPLOAD_FOLDER"])
        if isfile(os.path.join(app.config["UPLOAD_FOLDER"], f))
    ]


if __name__ == "__main__":
    app.run()
