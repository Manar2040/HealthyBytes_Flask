
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
    profile_image = db.Column(db.String(120), nullable=True, default='default-profile.png')
    favorites = db.relationship('Recipe', secondary=favorites,
                                backref=db.backref('favorited_by', lazy='dynamic'))
    reviews = db.relationship('Review', backref='author', lazy=True)
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True)

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
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    @property
    def review_count(self):
        return len(self.reviews)

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


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(30), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def _repr_(self):
        return f"Ingredient('{self.name}', '{self.quantity} {self.unit}')"


class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    meal_type = db.Column(db.String(10), nullable=False)  # breakfast, lunch, dinner, snack
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    recipe = db.relationship('Recipe', backref='meal_plans')

    def _repr_(self):
        return f"MealPlan('{self.day_of_week}', '{self.meal_type}')"