from flask_wtf import FlaskForm

from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

from app.validators import UserValidator


class RegisterForm(FlaskForm):
    first_name = StringField("first_name", validators=[
        DataRequired(),
        Length(1, 32)
    ])

    last_name = StringField("last_name", validators=[
        DataRequired(),
        Length(1, 32)
    ])

    email = EmailField("email", validators=[
        DataRequired(),
        Email(),
        UserValidator.check_unique_email()
    ])

    password = PasswordField("password", validators=[
        DataRequired(),
        UserValidator.validate_password(),
        Length(8, 16)
    ])

    password_confirmation = PasswordField("password_confirmation", validators=[
        DataRequired(),
        EqualTo("password")
    ])

    submit = SubmitField("submit")
