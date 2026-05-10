from flask import render_template, url_for
from app.models import Category, Recipe
from app.blueprints.categories import categories

@categories.route('/categories')
def all_categories():
    categories_list = Category.query.all()
    return render_template('categories.html', categories=categories_list)


@categories.route('/category/<int:category_id>')
def recipes_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    recipes = Recipe.query.filter_by(category_id=category_id).all()
    return render_template('recipes_by_category.html', category=category, recipes=recipes)