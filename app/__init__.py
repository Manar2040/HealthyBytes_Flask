from flask import Flask, request, session
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy
# pyrefly: ignore [missing-import]
from flask_login import LoginManager
# pyrefly: ignore [missing-import]
from flask_bcrypt import Bcrypt
# pyrefly: ignore [missing-import]
from flask_babel import Babel
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
babel = Babel()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max upload
    app.config['UPLOAD_FOLDER'] = 'app/static/images/profiles'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    def select_locale():
        # Check if language is specified in query parameters
        lang = request.args.get('lang')
        if lang in app.config['LANGUAGES']:
            session['lang'] = lang
            return lang
        # Check if language is stored in session
        return session.get('lang') or request.accept_languages.best_match(app.config['LANGUAGES'])
    
    babel.init_app(app, locale_selector=select_locale)

    # pyrefly: ignore [missing-import]
    from flask_babel import get_locale, format_number, format_decimal, format_date, format_datetime
    
    def to_arabic_nums(number):
        if get_locale().language != 'ar':
            return number
        
        western_nums = "0123456789"
        eastern_nums = "٠١٢٣٤٥٦٧٨٩"
        num_str = str(number)
        return num_str.translate(str.maketrans(western_nums, eastern_nums))

    @app.context_processor
    def inject_babel():
        return dict(
            get_locale=get_locale, 
            format_number=format_number, 
            format_decimal=format_decimal,
            format_date=format_date,
            format_datetime=format_datetime,
            ar_nums=to_arabic_nums
        )
    
    app.jinja_env.filters['ar_nums'] = to_arabic_nums

    from app.blueprints.auth import auth
    from app.blueprints.recipes import recipes
    from app.blueprints.categories import categories
    from app.blueprints.main import main
    from app.blueprints.planner import planner

    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    app.register_blueprint(categories)
    app.register_blueprint(main)
    app.register_blueprint(planner)


    from flask import render_template
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html',
                               code=404,
                               name="Page Not Found",
                               description="The page you're looking for doesn't exist."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html',
                               code=500,
                               name="Internal Server Error",
                               description="Something went wrong on our end."), 500


    return app