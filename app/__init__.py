from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.blueprints.auth import auth
    from app.blueprints.recipes import recipes
    from app.blueprints.categories import categories
    from app.blueprints.main import main

    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    app.register_blueprint(categories)
    app.register_blueprint(main)


    from flask import render_template
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html',
                               error_code=404,
                               error_message="Page Not Found",
                               error_description="The page you are looking for doesn't exist."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html',
                               error_code=500,
                               error_message="Internal Server Error",
                               error_description="Something went wrong on our end. Please try again later."), 500


    return app