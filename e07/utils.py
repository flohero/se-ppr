from flask import redirect, url_for


def create_error_page(error_msg: str):
    return redirect(
        url_for(
            "error",
            error=error_msg,
        )
    )
