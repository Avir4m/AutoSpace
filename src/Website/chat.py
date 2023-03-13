from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send
from Website import socketio

from .func import generate_key

chat = Blueprint("chats", __name__)

rooms = {}

@chat.route('/join-chat/',methods=['GET', 'POST'])
@login_required
def join_chat():
    name = current_user.username
    key = ""
    if request.method == 'POST':
        key = request.form.get('key')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        
        if not name:
            flash("Enter a name", category="error")
            return redirect(url_for('chats.join_chat'))
        
        if join != False and not key:
            flash("Enter a room key", category="error")
            return redirect(url_for('chats.join_chat'))
        
        room = key

        if create != False:
            room = generate_key(4)
            rooms[room] = {"members": 0, "messages": []}
        elif key not in rooms:
            flash("Room does not exists", category="error")
            return redirect(url_for('chats.join_chat'))

        session["room"] = room
        session["name"] = name
        return redirect(url_for("chats.group_chat"))

    return render_template('chats/join_chat.html', user=current_user, key=key)

@chat.route('/group-chat/')
@login_required
def group_chat():
    room = session.get('room')
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('chats.join_chat'))
    return render_template('chats/group_chat.html', user=current_user, room=room, messages=rooms[room]["messages"])


@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')

    if not room or not name:
        return
    if not room in rooms:
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
    if room not in rooms:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)