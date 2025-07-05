from flask import current_app, abort
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from enum import Enum

from app.database import engine

import socket


def send_welcome_email(user_email: str):
    mail = Mail(current_app)

    try:
        msg = Message(
            subject=f"Welcome to {current_app.config["APP_NAME"]}",
            recipients=[user_email],
            body=(
                "Hello my friend \n\n"
                "Your registration was successful! We hope you enjoy the task management program! ✅\n\n"
                "Good luck ✨"
            )
        )

        mail.send(msg)
    except (socket.gaierror, ConnectionRefusedError) as e:
        print(f"Error sending email :\n{e}")


def paginate(select_stmt, page: int = 1, per_page: int = 10):
    page = max(page, 1)
    offset = (page - 1) * per_page

    with Session(engine) as session:
        stmt = (
            select_stmt
            .offset(offset)
            .limit(per_page)
            .order_by(desc("created_at"))
        )

        items = session.execute(stmt).scalars().all()

        count_stmt = select_stmt.with_only_columns(func.count()).order_by(None)

        total = session.execute(count_stmt).scalar()

        total_pages = (total + per_page - 1) // per_page

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }


def get_task_status(enum_class: Enum, status_number: int):
    statuses = list(enum_class)

    for status in statuses:
        if status_number == status.value:
            return status.name

    return None


def show_task_status(enum_class: Enum):
    return list(enum_class)


def get_task_status_color(enum_class: Enum, status_number: int):
    status_colors = {
        "PENDING": "warning",
        "IN_PROGRESS": "info",
        "COMPLETED": "success",
        "CANCELED": "danger"
    }

    statuses = list(enum_class)

    for status in statuses:
        if status_number == status.value:
            return status_colors[status.name]

    return None


def encode(param):
    serialize = URLSafeSerializer(current_app.config["SECRET_KEY"])
    return serialize.dumps(param)


def decode(param):
    try:
        serialize = URLSafeSerializer(current_app.config["SECRET_KEY"])
        return serialize.loads(param)
    except Exception as e:
        print(e)
        abort(404)
