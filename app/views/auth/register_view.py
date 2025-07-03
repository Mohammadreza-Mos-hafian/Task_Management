from flask import render_template, redirect, url_for, request
from flask.views import MethodView

from app.forms import RegisterForm
from app.services import RegisterServiceLayer
from app.database import session_scope
from app.helpers import send_welcome_email


class RegisterView(MethodView):
    @staticmethod
    def get():
        form = RegisterForm()
        return render_template("auth/register.html", form=form)

    @staticmethod
    def post():
        form = RegisterForm()

        if form.validate_on_submit():
            service = RegisterServiceLayer(session_scope)

            service.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )

            send_welcome_email(form.email.data)

            return redirect(url_for("auth.login_view"))

        return render_template("auth/register.html", form=form)
