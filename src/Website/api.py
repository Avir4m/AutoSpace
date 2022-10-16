from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from .models import Forum, ForumMember, Post, Like, Saved, User, Follow, UserPreferences
from . import db


api = Blueprint('api', __name__)


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

@api.route('/user/<username>/settings/private_account', methods=['POST'])
@login_required
def private_account(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'oops..'}, 400)
    else:
        preferences = UserPreferences.query.filter_by(user_id=user.id).first()

        if preferences.private_account == True:
            preferences.private_account = False
            db.session.commit()
            return jsonify({'private_account': False})
        else:
            preferences.private_account = True
            db.session.commit()
            return jsonify({'private_account': True})



@api.route('/user/<username>/settings/get_preferences', methods=['POST'])
@login_required
def get_preferences(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'oops..'}, 400)
    else:
        preferences = UserPreferences.query.filter_by(user_id=user.id).first()

        return jsonify({'private_account': preferences.private_account})

@api.route('/remove-profile-picture/<username>', methods=['POST'])
def remove_profile_picture(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Post does not exist.'}, 400)
    else:
        user.picture = "default_profile_pic.jpg"
        db.session.commit()
        
    return jsonify({'picture': user.picture})