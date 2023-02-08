from flask import Blueprint, render_template, abort
from flask_login import current_user

admin = Blueprint("admin", __name__)

@admin.route("")
def adminHome():
    if current_user.permissions > 0:
        return render_template("admin/admin_home.html", user=current_user)
    abort(403)
