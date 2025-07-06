from flask import Blueprint
from app.views import CreateView, IndexView, EditView, DeleteView

task_bp = Blueprint("task", __name__, url_prefix="/task")

task_bp.add_url_rule("/create", view_func=CreateView.as_view("create_view"))
task_bp.add_url_rule("/index", view_func=IndexView.as_view("index_view"))
task_bp.add_url_rule("/edit/<id>", view_func=EditView.as_view("edit_view"))
task_bp.add_url_rule("/delete/<id>", view_func=DeleteView.as_view("delete_view"))
