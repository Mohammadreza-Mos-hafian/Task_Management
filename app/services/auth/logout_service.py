from flask_login import logout_user

from sqlalchemy import select, and_

from app.models import User


class LogoutServiceLayer:
    def __init__(self, session):
        self.session = session

    def logout(self, user_id: int):
        with self.session() as session:
            stmt = (
                select(User)
                .where(and_(
                    User.id == user_id,
                    User.is_deleted == False
                ))
            )

            user = session.execute(stmt).first()

            if user:
                logout_user()
                return True

        return False
