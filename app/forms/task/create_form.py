from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired

from wtforms import StringField, DateField, TextAreaField, MultipleFileField, SubmitField
from wtforms.validators import DataRequired, Length

from app.validators import TaskValidator, FileValidator


class CreateForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(1, 32)
    ])

    deadline = DateField("deadline", validators=[
        DataRequired(),
        TaskValidator.validate_date()
    ])

    files = MultipleFileField("files", validators=[
        FileAllowed(["jpg", "pdf", "docx", "jpeg", "png"]),
        FileValidator.validate_file_size()
    ])

    description = TextAreaField("description")

    submit = SubmitField("submit")
