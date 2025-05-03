
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User favorites association table
favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favorites = db.relationship('Recipe', secondary=favorites,
                                backref=db.backref('favorited_by', lazy='dynamic'))
    reviews = db.relationship('Review', backref='author', lazy=True)

    def _repr_(self):
        return f"User('{self.username}', '{self.email}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    recipes_count = db.Column(db.Integer, default=0)
    recipes = db.relationship('Recipe', backref='category', lazy=True)

    def _repr_(self):
        return f"Category('{self.name}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fats = db.Column(db.Float, nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default='default_recipe.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    reviews = db.relationship('Review', backref='recipe', lazy=True)

    def _repr_(self):
        return f"Recipe('{self.title}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def _repr_(self):
        return f"Review('{self.rating}')"