from flask import render_template
from app.models import Recipe, Category
from app.blueprints.main import main
from datetime import date


@main.route('/')
@main.route('/home')
def home():
    # Recipe of the Day — picks a consistent recipe based on today's date
    total = Recipe.query.count()
    if total > 0:
        day_index = date.today().toordinal() % total
        recipe_of_day = Recipe.query.offset(day_index).first()
    else:
        recipe_of_day = None

    # Top rated recipes for homepage (those with reviews)
    popular_recipes = Recipe.query.limit(4).all()

    return render_template('home.html', recipe_of_day=recipe_of_day, popular_recipes=popular_recipes)


@main.route('/about')
def about():
    return render_template('about.html', title='About Us')