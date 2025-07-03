from sqlalchemy import select, and_

from wtforms.validators import ValidationError

from werkzeug.security import check_password_hash

from app.database import session_scope
from app.enums import FlashMessage
from app.models import User

import re


class UserValidator:

    @staticmethod
    def check_unique_email():
        def _unique(form, field):
            if field.errors:
                return

            with session_scope() as session:
                stmt = (
                    select(User)
                    .where(
                        and_(
                            User.email == field.data,
                            User.is_deleted == False
                        )
                    )
                )

                if session.execute(stmt).first():
                    raise ValidationError("The email already exists.")

        return _unique

    @staticmethod
    def validate_password():
        pattern = r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'

        def _validate(form, field):
            if field.errors:
                return

            if not re.match(pattern, field.data):
                raise ValidationError("Password must be at least 8 characters long and contain at least one digit.")

        return _validate

    @staticmethod
    def validate_user_credentials():
        def _validate(form, field):
            if form.email.errors or form.password.errors:
                return

            with session_scope() as session:
                stmt = (
                    select(User)
                    .where(
                        and_(
                            User.email == form.email.data,
                            User.is_deleted == False
                        )
                    )
                )

                user: User = session.execute(stmt).scalar_one_or_none()

                if not user or not check_password_hash(user.password, form.password.data):
                    raise ValidationError(FlashMessage.LOGIN_FAILED.message())

        return _validate
