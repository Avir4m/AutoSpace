from flask import Blueprint, render_template, abort
from flask_login import current_user

from .models import User

chat = Blueprint("chats", __name__)

# WIP

@chat.route("/chat/<username>/")
def private_chat(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    return render_template("chats/chat.html", user=current_user)

@chat.route("/chat/<url>/<group_name>/")
def group_chat(url, group_name):
    return render_template("chats/chat.html", user=current_user)
