from flask import redirect, url_for, request
from flask_login import current_user

PUBLIC_ENDPOINTS = {
    "auth.register_view",
    "auth.login_view",
    "main_page"
}


def authenticate():
    endpoint = request.endpoint

    if endpoint == "static":
        return None

    if not current_user.is_authenticated and endpoint not in PUBLIC_ENDPOINTS:
        return redirect(url_for("main_page"))

    return None


def redirect_if_authenticated():
    endpoint = request.endpoint

    if endpoint == "static":
        return None

    if current_user.is_authenticated and endpoint in PUBLIC_ENDPOINTS:
        return redirect(url_for("dashboard.view"))

    return None
