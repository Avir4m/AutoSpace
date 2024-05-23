from flask import Blueprint, jsonify, current_app
from flask_login import current_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from .models import Notification, Space, SpaceMember, Post, Like, Saved, User, Follow, Friend
from . import db
import os

api = Blueprint("api", __name__)

# Spaces
@api.route("/join-space/<space_id>/", methods=["POST"])
@login_required
def join_space(space_id):
    space = Space.query.filter_by(id=space_id).first()
    member = SpaceMember.query.filter_by(user_id=current_user.id, space_id=space.id).first()

    if not space:
        return jsonify({"error": "Space does not exist."}, 400)
    elif member and space.creator != current_user.id:
        db.session.delete(member)
        db.session.commit()
    elif space.creator != current_user.id:
        member = SpaceMember(user_id=current_user.id, space_id=space.id)
        db.session.add(member)
        db.session.commit()

    return jsonify(
        {
            "members": len(space.members),
            "joined": current_user.id in map(lambda x: x.user_id, space.members),
        }
    )


# Posts
@api.route("/like-post/<post_id>/", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif like:
        notification = Notification.query.filter_by(like_id=like.id).first()
        db.session.delete(like)
        db.session.delete(notification)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.flush()
        notification = Notification(to=post.author, message=f"{ current_user.username } liked your post.", action_user=current_user.id, action="like", like_id=like.id)
        db.session.add(notification)
        db.session.commit()

    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id in map(lambda x: x.author, post.likes),
        }
    )


@api.route("/save-post/<post_id>/", methods=["POST"])
@login_required
def save_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    saved = Saved.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif saved:
        db.session.delete(saved)
        db.session.commit()
    else:
        saved = Saved(post_id=post_id, author=current_user.id)
        db.session.add(saved)
        db.session.commit()

    return jsonify({"saved": current_user.id in map(lambda x: x.author, post.saves)})


@api.route("/delete-post/<post_id>/", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return jsonify({"message": "post does not exist."})
    elif current_user.id != post.author and current_user.permissions < 1:
        return jsonify({"message": "you do not have permission to delete this post."})
    else:
        if post.comments:
            for comment in post.comments:
                db.session.delete(comment)
                db.session.commit()
        if post.likes:
            for like in post.likes:
                db.session.delete(like)
                db.session.commit()
        if post.saves:
            for saved in post.saves:
                db.session.delete(saved)
                db.session.commit()
        if post.reports:
            for report in post.reports:
                db.session.delete(report)
                db.session.commit()
        if post.picture:
            try:
                os.remove(os.getcwd()+ current_app.config["UPLOAD_FOLDER"]+ "/posts/"+ post.picture)
            except Exception as e:
                print(e)

        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Deleted post", "type": "success"})


# Users
@api.route("/follow/<username>/", methods=["POST"])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    followed = Follow.query.filter_by(
        follower_id=current_user.id, followed_id=user.id
    ).first()

    if not user or user.id == current_user.id:
        return jsonify({"error": "Post does not exist."}, 400)
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

    return jsonify(
        {
            "followers": len(user.followers),
            "followed": current_user.id in map(lambda x: x.follower_id, user.followers),
        }
    )


@api.route("/user/delete_account/<username>/<password>/", methods=["POST"])
def delete_account(username, password):
    if username != current_user.username:
        return jsonify({"message": "Wrong username", "type": "error"})

    user = User.query.filter_by(username=username).first()

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Wrong password.", "type": "error"})
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Done", "type": "success"})


@api.route("/user/change_password/<password>/<new_password>/", methods=["POST"])
def change_password(password, new_password):
    if " " in new_password:
        return jsonify({"message": "Password can't have spaces.", "type": "error"})
    elif len(new_password) < 7:
        return jsonify(
            {"message": "Password must be at least 7 characters.", "type": "error"}
        )
    elif check_password_hash(current_user.password, password):
        current_user.password = generate_password_hash(new_password, method="sha256")
        db.session.commit()
        return jsonify(
            {"message": "Your password has been changed.", "type": "success"}
        )
    else:
        return jsonify({"message": "Wrong password, please try again", "type": "error"})

@api.route("friend/<id>/", methods=["POST"])
def friend(id):
    user = User.query.filter_by(id=id).first()
    if user and user.id != current_user.id:
        sent_request = Friend.query.filter_by(user_id1=current_user.id, user_id2=user.id, status="pending").first()
        if sent_request:
            notification = Notification.query.filter_by(friend_id=sent_request.id).first()
            db.session.delete(notification)
            db.session.delete(sent_request)
            db.session.commit()
            return jsonify({"message": "Your friend request has been removed", "type": "success", "button": "Add Friend"})
        
        recive_request = Friend.query.filter_by(user_id1=user.id, user_id2=current_user.id, status="pending").first()
        if recive_request:
            recive_request.status = "friends"
            db.session.commit()
            return jsonify({"message": f"Accepted friend request", "type": "success", "button": "Remove Friend"})
        
        friends_added = Friend.query.filter_by(user_id1=current_user.id, user_id2=user.id, status="friends").first()
        friends_accepted = Friend.query.filter_by(user_id1=user.id, user_id2=current_user.id, status="friends").first()
        if friends_added or friends_accepted:
            if friends_added:
                db.session.delete(friends_added)
            else:
                db.session.delete(friends_accepted)
            db.session.commit()
            return jsonify({"message": f"You removed {user.username} from you friends list.", "type": "success", "button": "Add Friend"})

        request = Friend(user_id1=current_user.id, user_id2=user.id, status="pending")
        db.session.add(request)
        db.session.flush()
        notification = Notification(to=user.id, action_user=current_user.id, action="friend-request", message=f"{current_user.username} Sent you a friend request.", friend_id=request.id)
        db.session.add(notification)
        db.session.commit()
        return jsonify({"message": f"You have sent a friend request to {user.username}", "type": "success", "button": "Requested"})
    else:
        return jsonify({"message": "There is no user with that id.", "type": "error", "button": "Add Friend"})

@api.route("remove_request/<id>/", methods=["POST"])
def remove_request(id):
    user = User.query.filter_by(id=id).first()
    if user and id != current_user.id:
        recive_request = Friend.query.filter_by(user_id1=user.id, user_id2=current_user.id, status="pending").first()
        if recive_request:
            notification = Notification.query.filter_by(friend_id=recive_request.id).first()
            db.session.delete(notification)
            db.session.delete(recive_request)
            db.session.commit()
            return jsonify({"message": "Friend request has been removed", "type": "success", "button": "Add Friend"})

    return jsonify({"message": "No user with that id", "type": "error", "button": "Requested"})
