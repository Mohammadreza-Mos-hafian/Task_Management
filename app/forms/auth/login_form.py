from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.validators import UserValidator


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[
        DataRequired(),
        Email(),
        UserValidator.validate_user_credentials()
    ])

    password = PasswordField("password", validators=[
        DataRequired(),
    ])

    submit = SubmitField("submit")
