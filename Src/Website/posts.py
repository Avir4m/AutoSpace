from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .models import Post, Space
from .func import create_url, upload_file
from . import db

posts = Blueprint("posts", __name__)


@posts.route("/create-post/", methods=["POST", "GET"])
@login_required
def create_post():
    spaces = Space.query.filter_by().all()

    if request.method == "POST":
        title = request.form.get("post-title")
        text = request.form.get("post-text")
        spaceName = request.form.get("space")

        file = request.files["file"]

        space = Space.query.filter_by(name=spaceName).first()

        if not title:
            flash("Post title cannot be empty", category="error")
        elif len(title) >= 150:
            flash("Post title is too long.", category="error")
        elif not text:
            flash("Post text cannot be empty", category="error")
        elif not space and spaceName != None:
            flash("Space does not exist.", category="error")
        else:
            if spaceName == None:
                space_id = None
            else:
                space_id = space.id

            filename = upload_file(file, Post, "posts")

            post = Post(
                title=title,
                text=text,
                author=current_user.id,
                url=create_url(Post),
                space_id=space_id,
                picture=filename,
            )
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("posts/create_post.html", user=current_user, spaces=spaces)


@posts.route("/post-status/<post_id>/")
@login_required
def post_status(post_id):
    post = Post.query.filter_by(id=post_id).first()
    status = post.private
    if not post:
        flash("This post does not exist.", category="error")
    elif post.author != current_user.id:
        abort(403)
    elif status:
        post.private = False
        db.session.commit()
    else:
        post.private = True
        db.session.commit()

    return redirect(url_for("views.home"))

@posts.route("edit-post/<url>/", methods=["POST"])
@login_required
def edit_post(url):
    post = Post.query.filter_by(url=url).first()
    if not post:
        abort(404)
    elif post.author != current_user.id:
        flash("You are not allowed to edit this post.", category="error")
    else:
        new_post_title = request.form.get("newPostTitle")
        new_post_text = request.form.get("newPostText")

        if new_post_title == "":
            flash("Post title cannot be empty.", category="error")
        elif new_post_text == "":
            flash("Post text cannot be empty.", category="error")
        else:
            post.title = new_post_title
            post.text = new_post_text
            post.edited = True
            db.session.commit()
            flash("Post has been updated.", category="success")

    return redirect(url_for("views.home"))
