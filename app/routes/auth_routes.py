from flask import Blueprint
from app.views import RegisterView, LoginView, Logout

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.add_url_rule("/register", view_func=RegisterView.as_view("register_view"))
auth_bp.add_url_rule("/login", view_func=LoginView.as_view("login_view"))
auth_bp.add_url_rule("/logout", view_func=Logout.as_view("logout"))
