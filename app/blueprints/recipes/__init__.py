from flask import Blueprint

recipes = Blueprint('recipes', __name__)

from app.blueprints.recipes import routes