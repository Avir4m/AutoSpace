from flask import Blueprint, render_template, abort
from flask_login import current_user

from .models import Report

admin = Blueprint("admin", __name__)

@admin.route("")
def adminHome():
    if current_user.permissions > 0:
        return render_template("admin/admin_home.html", user=current_user)
    abort(403)

@admin.route("/reports")
def reports():
    if current_user.permissions > 0:
        reports = Report.query.filter_by().all()
        return render_template("admin/models/reports.html", user=current_user, reports=reports)
    abort(403)