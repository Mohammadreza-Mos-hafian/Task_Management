from flask_wtf import FlaskForm

from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from app.validators import TaskValidator
from app.enums import TaskStatus


class EditForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(1, 32)
    ])

    deadline = DateField("deadline", validators=[
        DataRequired(),
        TaskValidator.validate_date()
    ])

    description = TextAreaField("description")

    status = SelectField("status", validators=[
        DataRequired()
    ], choices=[
        (status.value, status.name) for status in list(TaskStatus)
    ])

    submit = SubmitField("submit")
