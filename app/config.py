from flask import Flask

from dotenv import load_dotenv

from datetime import datetime

import os

load_dotenv()


def creat_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
    TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        template_folder=TEMPLATES_DIR
    )

    app.config["app_name"] = os.getenv("APP_NAME")
    app.config["database"] = f"{os.getenv('DATABASE_URL').strip()}/{os.getenv('DATABASE_NAME').strip()}"
    app.config["secret_key"] = os.getenv("SECRET_KEY")
    app.config["debug"] = os.getenv("DEBUG") == "True"

    @app.context_processor
    def inject_config():
        return dict(
            config=app.config,
            year=datetime.now().year
        )

    return app
