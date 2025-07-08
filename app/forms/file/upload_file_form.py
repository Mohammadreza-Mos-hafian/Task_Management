from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired

from app.validators import FileValidator


class UploadFileForm(FlaskForm):
    files = MultipleFileField("upload_files", validators=[
        FileRequired(),
        FileAllowed(["jpg", "pdf", "docx", "jpeg", "png"]),
        FileValidator.validate_file_size()
    ])

    submit = SubmitField("upload")
