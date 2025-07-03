from flask import Blueprint

from app.views import DashboardView

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
dashboard_bp.add_url_rule("/home", view_func=DashboardView.as_view("view"))
