from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

from . import db
from .models import Notification, User
from .func import send_email, get_secret_key

auth = Blueprint("auth", __name__)

SECRET_KEY = get_secret_key()

s = URLSafeTimedSerializer(SECRET_KEY)

# Auth
@auth.route("/login/", methods=["GET", "POST"])
def login():
    email=""
    password=""
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if "check" in request.form:
            remember = True
        else:
            remember = False

        user = (
            User.query.filter_by(email=email).first()
            or User.query.filter_by(username=email).first()
        )
        if not user or not check_password_hash(user.password, password):
            flash("Invalid password or email address, Please try again.", category="error")
        elif len(password) <= 1:
            flash("You must enter your password.", category="error")
        else:
            flash("Logged in successfully!", category="success")
            login_user(user, remember=remember)
            return redirect(url_for("views.home"))

    return render_template("auth/login.html", user=current_user, email_username=email, password=password)


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    email = ""
    username = ""
    first_name = ""
    last_name = ""
    password1 = ""
    password2 = ""
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("userName")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif user_username:
            flash("Username already exists.", category="error")
        elif len(username) <= 1:
            flash("You must provide a username.", category="error")
        elif " " in username:
            flash("You cannot have spaces in username.", category="error")
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 character.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        elif " " in password1:
            flash("You cannot have spaces in password.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        else:
            new_user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1,  method='pbkdf2:sha256'),
            )
            db.session.add(new_user)
            db.session.flush()

            notification = Notification(to=new_user.id, action="Sign Up", message="Welcome to CarSpace")

            db.session.add(notification)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("auth/signup.html", user=current_user , email=email, username=username, firstname=first_name, lastname=last_name, password1=password1, password2=password2)


# Password
@auth.route("/forgot_password/", methods=["POST"])
def forgot_password():

    email = request.form.get("email")

    user = User.query.filter_by(email=email).first()

    if user:
        token = s.dumps(email, salt="reset-password")
        link = url_for("auth.reset_password", token=token, _external=True)
        msg = f"Email confirmation:\n {link}"
        sub = "Email confirmation"
        send_email(email, sub, msg)
        flash("Sent a verification link to your email address", category="success")
    else:
        flash(
            "This email is not connected to any account, please try different email addresses.",
            category="error",
        )

    return redirect(url_for("auth.login"))


@auth.route("/reset_password/<token>/", methods=["POST", "GET"])
def reset_password(token):
    try:
        email = s.loads(
            token, salt="reset-password", max_age=600
        )  # 600 Seconds (10 minutes)
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid token", category="error")
        if request.method == "POST":
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                flash("Passwords don't match..", category="error")
            elif len(password1) < 7:
                flash("Password must be at least 6 characters.", category="error")
            elif check_password_hash(user.password, password1):
                flash(
                    "New password can't be the same as the old one.",
                    category="error",
                )
            else:
                user.password = generate_password_hash(password1, method="sha256")
                db.session.commit()
                flash("Password has been changed!", category="success")
                return redirect(url_for("views.home"))
        return render_template("auth/reset_password.html", user=current_user)
    except SignatureExpired:
        abort(404)


# Email
@auth.route("/verify_email/")
def verify_email():
    user = current_user
    email = user.email

    token = s.dumps(email, salt="email-confirm")
    link = url_for("auth.confirm_email", token=token, _external=True)
    text = f"{link}"
    title = "Email confirmation"
    send_email(email, title, text)
    return redirect(url_for("users.dashboard", username=user.username))


@auth.route("/confirm_email/<token>/")
@login_required
def confirm_email(token):
    user = current_user
    try:
        email = s.loads(
            token, salt="email-confirm", max_age=3600
        )  # 3600 Seconds (1 Hour)
        if email == user.email:
            user.verified = True
            db.session.commit()
            flash("Your account is now verified!", category="success")
            return redirect(url_for("views.home"))
        else:
            abort(404)
    except SignatureExpired:
        abort(404)
