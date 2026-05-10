from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_babel import _

from flask_login import current_user, login_required
from app import db
from app.models import Recipe, Review, User, Category, Ingredient
from app.blueprints.recipes import recipes


@recipes.route('/recipes')
def all_recipes():
    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.paginate(page=page, per_page=8)
    return render_template('recipes.html', recipes=recipes_list)


@recipes.route('/search')
def search():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    min_cal = request.args.get('min_cal', type=int)
    max_cal = request.args.get('max_cal', type=int)
    sort_by = request.args.get('sort', 'title')

    filters = Recipe.query

    if query:
        filters = filters.filter(
            db.or_(
                Recipe.title.ilike(f'%{query}%'),
                Recipe.description.ilike(f'%{query}%')
            )
        )

    if category_id:
        filters = filters.filter_by(category_id=category_id)

    if min_cal is not None:
        filters = filters.filter(Recipe.calories >= min_cal)

    if max_cal is not None:
        filters = filters.filter(Recipe.calories <= max_cal)

    # Sorting
    if sort_by == 'calories_asc':
        filters = filters.order_by(Recipe.calories.asc())
    elif sort_by == 'calories_desc':
        filters = filters.order_by(Recipe.calories.desc())
    elif sort_by == 'protein':
        filters = filters.order_by(Recipe.protein.desc())
    elif sort_by == 'title':
        filters = filters.order_by(Recipe.title.asc())

    page = request.args.get('page', 1, type=int)
    results = filters.paginate(page=page, per_page=12)
    categories = Category.query.all()

    return render_template('search.html',
                           results=results,
                           categories=categories,
                           query=query,
                           category_id=category_id,
                           min_cal=min_cal,
                           max_cal=max_cal,
                           sort_by=sort_by)


@recipes.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    reviews = Review.query.filter_by(recipe_id=recipe_id).order_by(Review.date_posted.desc()).all()

    # Related recipes from same category (exclude current)
    related = Recipe.query.filter(
        Recipe.category_id == recipe.category_id,
        Recipe.id != recipe.id
    ).order_by(db.func.random()).limit(4).all()

    return render_template('recipe_detail.html', recipe=recipe, reviews=reviews, related=related)


@recipes.route('/recipe/<int:recipe_id>/review', methods=['POST'])
@login_required
def add_review(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    rating = request.form.get('rating')
    content = request.form.get('content')

    review = Review(rating=rating, content=content, author=current_user, recipe=recipe)
    db.session.add(review)
    db.session.commit()
    flash(_('Your review has been added!'), 'success')
    return redirect(url_for('recipes.recipe_detail', recipe_id=recipe_id))



@recipes.route('/favorites')
@login_required
def my_favorites():
    favorites = current_user.favorites
    return render_template('my_favorites.html', favorites=favorites)


@recipes.route('/toggle_favorite/<int:recipe_id>', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    """AJAX endpoint to toggle favorites without page reload."""
    recipe = Recipe.query.get_or_404(recipe_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if recipe in current_user.favorites:
        current_user.favorites.remove(recipe)
        db.session.commit()
        if is_ajax:
            return jsonify({'status': 'removed', 'message': _('Removed from favorites')})
        flash(_('Recipe removed from favorites!'), 'success')

    else:
        current_user.favorites.append(recipe)
        db.session.commit()
        if is_ajax:
            return jsonify({'status': 'added', 'message': _('Added to favorites!')})
        flash(_('Recipe added to favorites!'), 'success')


    return redirect(url_for('recipes.recipe_detail', recipe_id=recipe_id))


@recipes.route('/add_to_favorites/<int:recipe_id>', methods=['POST'])
@login_required
def add_to_favorites(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.favorites:
        flash(_('This recipe is already in your favorites!'), 'info')

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


@recipes.route('/pantry', methods=['GET', 'POST'])
def pantry():
    # 1. Get all unique ingredient names to populate the selection interface
    all_ingredients_query = db.session.query(Ingredient.name).distinct().all()
    # Clean and sort ingredient names
    all_ingredients = sorted(list(set([ing[0].lower().strip() for ing in all_ingredients_query])))

    user_ingredients = []
    matched_recipes = []

    if request.method == 'POST':
        # Get list of ingredients selected by the user
        user_ingredients = request.form.getlist('ingredients')
        user_ingredients_lower = [ing.lower().strip() for ing in user_ingredients]

        if user_ingredients_lower:
            # 2. Logic: Calculate Match Score for every recipe
            recipes = Recipe.query.all()
            for recipe in recipes:
                if not recipe.ingredients:
                    continue
                
                recipe_ingredient_names = [ing.name.lower().strip() for ing in recipe.ingredients]
                total_recipe_ingredients = len(recipe_ingredient_names)
                
                # How many of the recipe's ingredients does the user have?
                matches = [ing for ing in recipe_ingredient_names if ing in user_ingredients_lower]
                match_count = len(matches)
                missing = [ing.title() for ing in recipe_ingredient_names if ing not in user_ingredients_lower]
                
                # Only include if they have at least 1 matching ingredient
                if match_count > 0:
                    match_percentage = int((match_count / total_recipe_ingredients) * 100)
                    matched_recipes.append({
                        'recipe': recipe,
                        'match_percentage': match_percentage,
                        'match_count': match_count,
                        'total_ingredients': total_recipe_ingredients,
                        'missing': missing
                    })
            
            # Sort by match percentage (descending)
            matched_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)

    return render_template('pantry.html', 
                           all_ingredients=all_ingredients, 
                           user_ingredients=user_ingredients,
                           matched_recipes=matched_recipes)