from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required

from .models import Report

admin = Blueprint("admin", __name__)

@admin.route("/")
@login_required
def adminHome():
    if current_user.permissions > 0:
        return render_template("admin/admin_home.html", user=current_user)
    abort(403)

@admin.route("/reports/posts/")
@login_required
def posts_reports():
    if current_user.permissions > 0:
        reports = Report.query.filter_by(comment_id=None, space_id=None).all()
        return render_template("admin/models/post_reports.html", user=current_user, reports=reports)
    abort(403)

@admin.route("/reports/comments/")
@login_required
def comments_reports():
    if current_user.permissions > 0:
        reports = Report.query.filter_by(post_id=None, space_id=None).all()
        return render_template("admin/models/comment_reports.html", user=current_user, reports=reports)
    abort(403)

@admin.route("/reports/spaces/")
@login_required
def spaces_reports():
    if current_user.permissions > 0:
        reports = Report.query.filter_by(comment_id=None, post_id=None).all()
        return render_template("admin/models/space_reports.html", user=current_user, reports=reports)
    abort(403)