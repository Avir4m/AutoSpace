from flask import Blueprint, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .models import Post, Report, Space, Comment
from . import db

reports = Blueprint("reports", __name__)


@reports.route("/create-report/post/<url>/", methods=["POST"])
@login_required
def report_post(url):
    post = Post.query.filter_by(url=url).first()
    if not post:
        abort(404)

    description = request.form.get("description")
    reason = request.form.get("reason")

    report = Report(
        description=description, reason=reason, author=current_user.id, post_id=post.id
    )
    db.session.add(report)
    db.session.commit()
    flash("Post has been reported!", category="success")
    return redirect(url_for("views.home"))


@reports.route("/create-report/space/<url>/", methods=["POST"])
@login_required
def report_space(url):
    space = Space.query.filter_by(url=url).first()
    if not space:
        abort(404)

    description = request.form.get("description")
    reason = request.form.get("reason")

    report = Report(
        description=description,
        reason=reason,
        author=current_user.id,
        space_id=space.id,
    )
    db.session.add(report)
    db.session.commit()
    flash("Forum has been reported!", category="success")
    return redirect(url_for("views.home"))


@reports.route("/create-report/comment/<id>/", methods=["POST"])
@login_required
def report_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        abort(404)

    description = request.form.get("description")
    reason = request.form.get("reason")

    report = Report(
        description=description, reason=reason, author=current_user.id, comment_id=id
    )
    db.session.add(report)
    db.session.commit()
    flash("Comment has been reported!", category="success")
    return redirect(url_for("views.home"))


@reports.route("/delete-report/<id>/")
@login_required
def delete_report(id):
    if current_user.permissions < 1:
        abort(403)
    report = Report.query.filter_by(id=id).first()
    if not report:
        abort(404)

    db.session.delete(report)
    db.session.commit()
    flash("Report has been deleted!", category="success")
    return redirect(url_for("admin.adminHome"))