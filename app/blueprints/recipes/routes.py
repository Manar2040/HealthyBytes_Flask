from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Recipe, Review, User
from app.blueprints.recipes import recipes


@recipes.route('/recipes')
def all_recipes():
    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.paginate(page=page, per_page=8)
    return render_template('recipes.html', recipes=recipes_list)


@recipes.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    reviews = Review.query.filter_by(recipe_id=recipe_id).all()
    return render_template('recipe_detail.html', recipe=recipe, reviews=reviews)


@recipes.route('/recipe/<int:recipe_id>/review', methods=['POST'])
@login_required
def add_review(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    rating = request.form.get('rating')
    content = request.form.get('content')

    review = Review(rating=rating, content=content, author=current_user, recipe=recipe)
    db.session.add(review)
    db.session.commit()
    flash('Your review has been added!', 'success')
    return redirect(url_for('recipes.recipe_detail', recipe_id=recipe_id))


@recipes.route('/favorites')
@login_required
def my_favorites():
    favorites = current_user.favorites
    return render_template('my_favorites.html', favorites=favorites)


@recipes.route('/add_to_favorites/<int:recipe_id>', methods=['POST'])
@login_required
def add_to_favorites(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.favorites:
        flash('This recipe is already in your favorites!', 'info')
    else:
        current_user.favorites.append(recipe)
        db.session.commit()
        flash('Recipe added to favorites!', 'success')
    return redirect(url_for('recipes.recipe_detail', recipe_id=recipe_id))


@recipes.route('/remove_from_favorites/<int:recipe_id>', methods=['POST'])
@login_required
def remove_from_favorites(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.favorites:
        current_user.favorites.remove(recipe)
        db.session.commit()
        flash('Recipe removed from favorites!', 'success')
    return redirect(url_for('recipes.my_favorites'))