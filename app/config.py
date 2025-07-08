from flask import Flask, flash, request, redirect, url_for
from flask_login import LoginManager

from dotenv import load_dotenv

from datetime import datetime

from werkzeug.exceptions import RequestEntityTooLarge

from app.routes import auth_bp, dashboard_bp, task_bp, file_bp
from app.models import User
from app.enums import TaskStatus
from app.helpers import get_task_status, show_task_status, get_task_status_color, encode

from urllib.parse import urlparse

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

    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER").strip()
    app.config['MAIL_PORT'] = int(os.getenv("mail_port").strip())
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME").strip()
    app.config['MAIL_PASSWORD'] = os.getenv("mail_password").strip()
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("mail_default_sender").strip()

    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

    app.config["DEBUG"] = os.getenv("DEBUG") == "True"

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(file_bp)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        flash(f"Uploaded file is too large! (Max size: {app.config["MAX_CONTENT_LENGTH"] // (1024 ** 2)} MB).",
              "danger")

        ref = request.referrer

        if ref:
            path = urlparse(ref).path

            if path.endswith("/create"):
                path = path.replace("/create", "/index")

            return redirect(path)

        return redirect(url_for("dashboard.view"))

    @app.context_processor
    def inject_config():
        return dict(
            config=app.config,
            year=datetime.now().year,
            TaskStatus=TaskStatus,
            get_task_status=get_task_status,
            get_task_status_color=get_task_status_color,
            encode=encode
        )

    return app
