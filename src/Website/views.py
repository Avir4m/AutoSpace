from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from .models import Forum, Post


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    posts = Post.query.filter_by().all()
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