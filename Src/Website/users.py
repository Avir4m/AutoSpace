from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user

import os

from .models import Follow, Notification, User, Post, User
from .func import upload_file
from . import db

users = Blueprint("users", __name__)

@users.route("/user/<username>/dashboard/", methods=["POST", "GET"])
@login_required
def dashboard(username):
    if username == current_user.username:
        if request.method == "POST":
            
            user = current_user
            
            email = request.form.get("email")
            username = request.form.get("userName")
            first_name = request.form.get("firstName")
            last_name = request.form.get("lastName")
            description = request.form.get("description")
            
            file = request.files["file"]

            if file:
                filename = upload_file(file, User, "users")
                if user.picture != "default_profile_pic.jpg":
                    try:
                        os.remove(os.getcwd() + current_app.config["UPLOAD_FOLDER"] + "/users/" + user.picture)
                    except:
                        print("Could not remove picture..")
                user.picture = filename
                db.session.commit()
            
            user_email = User.query.filter_by(email=email).first()
            user_name = User.query.filter_by(username=username).first()
            
            if user_email:
                if email == user.email:
                    pass
                else:
                    flash("This email is already in use.", category="error")
            if user_name:
                if username == user.username:
                    pass
                else:
                    flash("This username is already in use.", category="error")
            if email == user.email and username == user.username and first_name == user.first_name and last_name == user.last_name and description == user.description and not file:
                flash("Can\"t update profile if nothing has been changed.", category="error")
            
            else:
                if first_name == "":
                    flash("First Name must be provided.", category="error")
                elif username == "":
                    flash("Username must be provided.", category="error")
                elif email == "":
                    flash("Email must be provided.", category="error")
                elif " " in username:
                    flash("You cannot have spaces in username.", category="error")
                else:
                    user.email = email
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.description = description
                    db.session.commit()
                    flash("Profile has been updated.", category="success")
                
        return render_template("users/dashboard.html", user=current_user)
    
    else:
        return redirect(url_for("views.dashboard"), username=current_user.username)

@users.route("/user/<username>/saved/")
@login_required
def saved(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        abort(404)
    
    posts = Post.query.join(Post.saves).filter_by(author=user.id).all()
    
    return render_template("users/saved.html", user=current_user, posts=posts)

@users.route("/user/<username>/liked/")
@login_required
def liked(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        abort(404)
    
    posts = Post.query.join(Post.likes).filter_by(author=user.id).all()
    
    return render_template("users/liked.html", user=current_user, posts=posts)

@users.route("/follow/<username>/")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    followed = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=user.id
    ).first()

    if not user or user.id == current_user.id:
        flash("Can't do that")
        return redirect(url_for("views.home"))
    elif followed:
        notification = Notification.query.filter_by(action="follow", to=user.id, action_user=current_user.id).first()
        db.session.delete(notification)
        db.session.delete(followed)
        db.session.commit()
    else:
        notification = Notification(to=user.id, message=f"{ current_user.username } started following you.", action_user=current_user.id, action="follow")
        follow = Follow(follower_id=current_user.id, followed_id=user.id)
        db.session.add(follow)
        db.session.add(notification)
        db.session.commit()

    return redirect(url_for("views.home"))