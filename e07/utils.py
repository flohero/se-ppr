from flask import redirect, url_for


def create_error_page(error_msg: str):
    return redirect(
        url_for(
            "error",
            error=error_msg
        )
    )


def file_does_not_exist_error():
    return create_error_page(f"File does not exist")

