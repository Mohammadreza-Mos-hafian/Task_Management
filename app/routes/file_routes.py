from flask import Blueprint
from app.views import FileView, DeleteFileView, DownloadView

file_bp = Blueprint("file", __name__, url_prefix="/file")

file_bp.add_url_rule("/index/<id>", view_func=FileView.as_view("index_view"))
file_bp.add_url_rule("/delete/<id>", view_func=DeleteFileView.as_view("delete_view"))
file_bp.add_url_rule("/download/<id>", view_func=DownloadView.as_view("download_view"))
