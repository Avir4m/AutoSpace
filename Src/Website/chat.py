from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send
from Website import socketio

from .func import generate_key
from .models import Chat, ChatMessage
from . import db

chat = Blueprint("chats", __name__)

@chat.route('/join-chat/',methods=['GET', 'POST'])
@login_required
def join_chat():
    key = ""
    if request.method == 'POST':
        key = request.form.get('key')
        join = request.form.get('join', False)
        create = request.form.get('create', False)
        
        if join != False and not key:
            flash("Enter a room key", category="error")
            return redirect(url_for('chats.join_chat'))
        
        room = key

        if create != False:
            chat = Chat()
            db.session.add(chat)
            db.session.flush()
            room = chat.id
            db.session.commit()
        elif not Chat.query.filter_by(id=key).first():
            flash("Room does not exists", category="error")
            return redirect(url_for('chats.join_chat'))

        session["room"] = room
        session["name"] = current_user.username
        return redirect(url_for("chats.group_chat"))

    return render_template('chats/join_chat.html', user=current_user, key=key)

@chat.route('/group-chat/')
@login_required
def group_chat():
    room = session.get('room')
    chat = Chat.query.filter_by(id=room).first()
    if room is None or not chat:
        return redirect(url_for('chats.join_chat'))

    return render_template('chats/group_chat.html', user=current_user, room=room, messages=chat.messages)


@socketio.on('connect')
def connect(auth):
    room = session.get('room')

    if not Chat.query.filter_by(id=room).first():
        leave_room(room)
        return
    
    join_room(room)

@socketio.on('disconnect')
def disconnect():
    room = session.get("room")
    leave_room(room)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if not Chat.query.filter_by(id=room).first():
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    message = ChatMessage(chat_id=room, author=current_user.id, message=data["data"])
    db.session.add(message)
    db.session.commit()