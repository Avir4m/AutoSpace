from flask import Blueprint, render_template
from flask_login import current_user, login_required
from flask_socketio import send

from . import socketio


chat = Blueprint('chat', __name__)


@login_required
@chat.route('/test/')
def test():
    return render_template('chats/chat.html', user=current_user)


@socketio.on('message')
def handleMessage(msg):
        send(msg, broadcast=True)