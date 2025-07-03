from flask import Flask
from flask_login import LoginManager

from dotenv import load_dotenv

from datetime import datetime

from app.routes import auth_bp, dashboard_bp
from app.models import User

import os

load_dotenv()


def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
    TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")

    app = Flask(
        __name__,
        static_folder=STATIC_DIR,
        template_folder=TEMPLATES_DIR
    )

    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login_view"
    login_manager.login_message_category = "info"

    login_manager.user_loader(User.load_user)

    app.config["APP_NAME"] = os.getenv("APP_NAME")
    app.config["DATABASE"] = f"{os.getenv('DATABASE_URL').strip()}/{os.getenv('DATABASE_NAME').strip()}"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["DEBUG"] = os.getenv("DEBUG") == "True"

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.context_processor
    def inject_config():
        return dict(
            config=app.config,
            year=datetime.now().year
        )

    return app
