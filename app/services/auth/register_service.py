from werkzeug.security import generate_password_hash

from app.models import User


class RegisterServiceLayer:
    def __init__(self, session):
        self.session = session

    def register(self, first_name: str, last_name: str, email: str, password: str):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password, salt_length=16)
        )

        with self.session() as session:
            session.add(user)
