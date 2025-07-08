from flask import current_app
from wtforms.validators import ValidationError

import os


class FileValidator:
    @staticmethod
    def validate_file_size():
        def _file_size(form, field):
            files = field.data

            if not files:
                raise ValidationError("No files selected.")

            max_total_size = current_app.config["MAX_CONTENT_LENGTH"]
            total_size = 0

            for f in files:
                f.seek(0, os.SEEK_END)
                total_size += f.tell()
                f.seek(0)

            if total_size > max_total_size:
                raise ValidationError(f"Total size exceeds {max_total_size / (1024 * 1024):.1f} MB.")

        return _file_size
