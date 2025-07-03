from flask import current_app
from flask_mail import Mail, Message

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
