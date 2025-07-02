from flask import render_template

from app import creat_app

app = creat_app()


@app.route("/", endpoint="main_page")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
