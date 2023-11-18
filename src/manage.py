import logging

from flask import Flask
from app import constants
from app.blueprints.home import bp as home_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.categories import bp as categories_bp
from app.blueprints.search import bp as search_bp

from models.auth import User
from models.commerce import Advert, Category, Search

from settings import config
from extensions import db, login_manager


logging.basicConfig(level=logging.INFO)


def create_app():
    app_ = Flask(
        __name__,
        instance_relative_config=True,
    )
    app_.config.from_object(config)

    app_.register_blueprint(home_bp)
    app_.register_blueprint(auth_bp)
    app_.register_blueprint(categories_bp)
    app_.register_blueprint(search_bp)

    db.init_app(app_)
    return app_, db


app_, db = create_app()
login_manager.init_app(app_)


@app_.context_processor
def inject_categories():
    return dict(categories=constants.CATEGORY_NAMES)


with app_.app_context():
    print("Models created!")
    db.create_all()


if __name__ == "__main__":
    app_.run(debug=True, host="0.0.0.0")
