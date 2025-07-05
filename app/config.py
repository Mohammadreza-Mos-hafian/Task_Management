from flask import Flask
from flask_login import LoginManager

from dotenv import load_dotenv

from datetime import datetime

from app.routes import auth_bp, dashboard_bp, task_bp
from app.models import User
from app.enums import TaskStatus
from app.helpers import get_task_status, show_task_status, get_task_status_color, encode

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

    app.config["DEBUG"] = os.getenv("DEBUG") == "True"

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(task_bp)

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
