from flask import Flask



def create_app():
    app = Flask(__name__)



    from app.blueprints.auth import auth
    from app.blueprints.recipes import recipes
    from app.blueprints.categories import categories
    from app.blueprints.main import main

    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    app.register_blueprint(categories)
    app.register_blueprint(main)




    return app