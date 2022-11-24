from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import desc

from .models import Forum, Post, User

views = Blueprint('views', __name__)


@views.route('/')
def home():
    posts = Post.query.order_by(desc(Post.date_created)).all()
    return render_template('home.html', user=current_user, posts=posts)


@views.route('/post/<url>/')
def post(url):
    post = Post.query.filter_by(url=url).first()
    posts = Post.query.filter_by(url=url).all()
    if not post:
        abort(404)
    else:
        return render_template('posts/post.html', post=post, user=current_user, posts=posts)
    
@views.route('/forum/<url>/')
def forum(url):
    forum = Forum.query.filter_by(url=url).first()
    posts = Post.query.filter_by(forum_id=forum.id).all()
    
    if not forum:
        abort(404)
    else:
        return render_template('forums/forum.html', user=current_user, forum=forum, posts=posts)

@views.route('/user/<username>/')
def user(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("users/user.html", user=current_user, posts=posts, username=user)