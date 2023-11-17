from flask import Blueprint, render_template, request, session, redirect
from flask_login import login_user
from models.auth import User
from extensions import db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("login-email")).first()
        if user and user.password == request.form.get("login-pass"):
            login_user(user)
            print(f"You are now logged in as {user.email}")
            return redirect("/")
        else:
            print("User not found")
    return render_template("auth/login.html")


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["signup-email"]
        password = request.form["signup-pass"]
        user = User(email, password)
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            print(f"User with email {email} already exists")
            return redirect("signup")
        db.session.add(user)
        db.session.commit()
        return redirect("login")

    return render_template("auth/signup.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
