from wtforms.validators import ValidationError

from datetime import datetime, date


class TaskValidator:
    @staticmethod
    def validate_date():
        def _date(form, field):
            task = getattr(form, "_task_instance", None)

            if isinstance(field.data, datetime):
                field_date = field.data.date()
            else:
                field_date = field.data

            if task and field_date == task.deadline:
                return

            if field_date < date.today():
                raise ValidationError(f"The deadline cannot be before {date.today().strftime('%Y-%m-%d')}")

        return _date
