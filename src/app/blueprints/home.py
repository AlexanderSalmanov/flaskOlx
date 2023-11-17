from flask import Blueprint, render_template


bp = Blueprint("hello", __name__, url_prefix="/")


@bp.route("/")
def hello():
    return render_template("home.html")
