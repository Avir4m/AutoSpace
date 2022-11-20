from flask import Blueprint, jsonify, redirect, url_for, current_app
from flask_login import current_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from .models import Forum, ForumMember, Post, Like, Saved, User, Follow
from . import db
import os

api = Blueprint('api', __name__)


# Forums
@api.route('/join-forum/<forum_id>/', methods=['POST'])
@login_required
def join_forum(forum_id):
    forum = Forum.query.filter_by(id=forum_id).first()
    member = ForumMember.query.filter_by(user_id=current_user.id, forum_id=forum.id).first()
    
    if not forum:
        return jsonify({'error': 'Forum does not exist.'}, 400)
    elif member and forum.creator != current_user.id:
            db.session.delete(member)
            db.session.commit()
    elif forum.creator != current_user.id:
        member = ForumMember(user_id=current_user.id, forum_id=forum.id)
        db.session.add(member)
        db.session.commit()
        
    return jsonify({'members': len(forum.members), 'joined': current_user.id in map(lambda x: x.user_id, forum.members)})


# Posts
@api.route('/like-post/<post_id>/', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        
    return jsonify({'likes': len(post.likes), 'liked': current_user.id in map(lambda x: x.author, post.likes)})

@api.route('/save-post/<post_id>/', methods=['POST'])
@login_required
def save_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    saved = Saved.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif saved:
        db.session.delete(saved)
        db.session.commit()
    else:
        saved = Saved(post_id=post_id, author=current_user.id)
        db.session.add(saved)
        db.session.commit()
        
    return jsonify({'saved': current_user.id in map(lambda x: x.author, post.saves)})

@api.route('/delete-post/<post_id>/', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({'message':'post does not exist.'})
    elif current_user.id != post.author and current_user.permissions <= 1:
        return jsonify({'message':'you do not have permission to delete this post.'})
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
                os.remove(os.getcwd() + current_app.config['UPLOAD_FOLDER'] + '/posts/' + post.picture)
            except Exception as e:
                print(e)
                
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Deleted post', 'type': 'success'})

# Users
@api.route('/follow/<username>/', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    followed = Follow.query.filter_by(follower_id=current_user.id, followed_id=user.id).first()
    
    if not user or user.id == current_user.id:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif followed:
        db.session.delete(followed)
        db.session.commit()
    else:
        follow = Follow(follower_id=current_user.id, followed_id=user.id)
        db.session.add(follow)
        db.session.commit()
        
    return jsonify({'followers': len(user.followers), 'followed': current_user.id in map(lambda x: x.follower_id, user.followers)})

@api.route('/user/delete_account/<username>/<password>', methods=['POST'])
def delete_account(username, password):
    if username != current_user.username:
        return jsonify({'message': 'Wrong username', 'type': 'error'})

    user = User.query.filter_by(username=username).first()

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Wrong password.', 'type': 'error'})
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Done', 'type': 'success'})

@api.route('/user/change_password/<password>/<new_password>', methods=['POST'])
def change_password(password, new_password):
    if ' ' in new_password:
        return jsonify({'message': 'Password can\'t have spaces.', 'type': 'error'})
    elif len(new_password) < 7:
        return jsonify({'message': 'Password must be at least 7 characters.', 'type': 'error'})
    elif check_password_hash(current_user.password, password):
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        return jsonify({'message': 'Your password has been changed.', 'type': 'success'})
    else:
        return jsonify({'message': 'Wrong password, please try again', 'type': 'error'})