from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import DevelopmentConfig, ProductionConfig


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .models import Menu, Sell, User
        db.create_all()

    from .public import public_bp
    from .auth import auth_bp
    from .cart import cart_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)

    register_error_handlers(app)

    return app


app = create_app()
