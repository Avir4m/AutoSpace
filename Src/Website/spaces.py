from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user

import os

from .models import Space, SpaceMember
from .func import create_url, upload_file
from . import db

spaces = Blueprint("spaces", __name__)

@spaces.route("/create-space/", methods=["POST", "GET"])
@login_required
def create_space():
    if request.method == "POST":
        name = request.form.get("spaceName")
        description = request.form.get("spaceDescription")
        
        space = Space.query.filter_by(name=name).first()
        
        file = request.files["file"]
        
        if space:
            flash("space name already exists, please change space name.", category="error")
        elif len(name) <= 2:
            flash("space name must be at least 2 characters", category="error")
        else:

            filename = upload_file(file, Space, "spaces")

            space = Space(name=name, description=description, creator=current_user.id, url=create_url(Space), picture=filename)

            db.session.add(space)
            db.session.commit()
            
            db.session.refresh(space)
            spaceMember = SpaceMember(user_id=current_user.id, space_id=space.id)
            db.session.add(spaceMember)
            db.session.commit()
            
            flash("space created successfully!", category="success")
            return redirect(url_for("views.home"))
        
    return render_template("spaces/create_space.html", user=current_user)
    
@spaces.route("/delete-space/<space_id>/")
@login_required
def delete_space(space_id):
    space = Space.query.filter_by(id=space_id).first()
    
    if not space:
        flash("space does not exists.", category="error")
    elif current_user.id != space.creator and current_user.permissions < 1:
        flash("you do not have permission to delete this space.", category="error")
    else:
        if space.reports:
            for report in space.reports:
                db.session.delete(report)
                db.session.commit()
        if space.members:
            for member in space.members:
                db.session.delete(member)
                db.session.commit()
        if space.picture:
            try:
                os.remove(os.getcwd() + current_app.config["UPLOAD_FOLDER"] + "/spaces/" + space.picture)
            except:
                print("Could not remove picture..")
                
        db.session.delete(space)
        db.session.commit()
        flash("space has been deleted.", category="success")
        
    return redirect(url_for("views.home"))

@spaces.route("/edit-space/<space_id>/", methods=["POST"])
@login_required
def edit_space(space_id):
    space = Space.query.filter_by(id=space_id).first()
    
    if not space:
        abort(404)
    if not space:
        flash("space does not exists.", category="error")
    elif current_user.id != space.creator:
        flash("you do not have permission to delete this space.", category="error")
    else:
        new_name = request.form.get("newName")
        new_description = request.form.get("newDescription")
        
        file = request.files["file"]
    
        filename = upload_file(file, Space, "spaces")
        if space.picture:
            try:
                os.remove(os.getcwd() + current_app.config["UPLOAD_FOLDER"] + "/spaces/" + space.picture)
            except:
                pass
        space.picture = filename
        db.session.commit()
        
        if len(new_name) <= 2:
            flash("space name must be at least 2 characters.", category="error")
        else:
            space.name = new_name
            space.description = new_description
            space.edited = True
            db.session.commit()
            flash("space has been updated.", category="success")
            return redirect(url_for("views.space", url=space.url))

