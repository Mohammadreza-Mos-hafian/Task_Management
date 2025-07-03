from flask_login import login_user

from sqlalchemy import select

from app.models import User
from app.database import engine


class LoginServiceLayer:
    def __init__(self, session):
        self.session = session

    def login(self, email: str):
        with self.session(engine) as session:
            stmt = (
                select(User)
                .where(User.email == email)
            )

            user: User = session.execute(stmt).scalar_one_or_none()

            if user:
                login_user(user)
