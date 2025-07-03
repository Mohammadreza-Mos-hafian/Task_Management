from flask import render_template

from app import create_app
from app.middlewares import authenticate, redirect_if_authenticated

app = create_app()


@app.before_request
def apply_middleware():
    for middleware in [authenticate, redirect_if_authenticated]:
        response = middleware()

        if response:
            return response

    return None


@app.route("/", endpoint="main_page")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
