from flask_wtf import FlaskForm

from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from app.validators import TaskValidator


class CreateForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(1, 32)
    ])

    deadline = DateField("deadline", validators=[
        DataRequired(),
        TaskValidator.validate_date()
    ])

    description = TextAreaField("description")

    submit = SubmitField("submit")
