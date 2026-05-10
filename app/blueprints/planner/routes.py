from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_babel import _

from flask_login import login_required, current_user
from app import db
from app.models import MealPlan, Recipe, Category
from app.blueprints.planner import planner


DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack']


@planner.route('/meal-planner')
@login_required
def meal_planner():
    # Get user's meal plan entries
    meal_entries = MealPlan.query.filter_by(user_id=current_user.id).all()

    # Organize into a grid: {day: {meal_type: [recipes]}}
    plan_grid = {}
    for day in DAYS_OF_WEEK:
        plan_grid[day] = {}
        for meal_type in MEAL_TYPES:
            plan_grid[day][meal_type] = []

    for entry in meal_entries:
        if entry.day_of_week in plan_grid and entry.meal_type in plan_grid[entry.day_of_week]:
            plan_grid[entry.day_of_week][entry.meal_type].append(entry)

    # Calculate daily totals
    daily_totals = {}
    for day in DAYS_OF_WEEK:
        total_cal = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        for meal_type in MEAL_TYPES:
            for entry in plan_grid[day][meal_type]:
                if entry.recipe:
                    total_cal += entry.recipe.calories or 0
                    total_protein += entry.recipe.protein or 0
                    total_carbs += entry.recipe.carbs or 0
                    total_fats += entry.recipe.fats or 0
        daily_totals[day] = {
            'calories': total_cal,
            'protein': round(total_protein, 1),
            'carbs': round(total_carbs, 1),
            'fats': round(total_fats, 1)
        }

    # Get all recipes for the "add" dropdown
    all_recipes = Recipe.query.order_by(Recipe.title).all()
    categories = Category.query.all()

    return render_template('meal_planner.html',
                           plan_grid=plan_grid,
                           days=DAYS_OF_WEEK,
                           meal_types=MEAL_TYPES,
                           daily_totals=daily_totals,
                           all_recipes=all_recipes,
                           categories=categories)


@planner.route('/meal-planner/add', methods=['POST'])
@login_required
def add_to_plan():
    recipe_id = request.form.get('recipe_id', type=int)
    day = request.form.get('day')
    meal_type = request.form.get('meal_type')

    if not recipe_id or day not in DAYS_OF_WEEK or meal_type not in MEAL_TYPES:
        flash(_('Invalid selection.'), 'danger')
        return redirect(url_for('planner.meal_planner'))


    recipe = Recipe.query.get_or_404(recipe_id)

    entry = MealPlan(
        user_id=current_user.id,
        recipe_id=recipe.id,
        day_of_week=day,
        meal_type=meal_type
    )
    db.session.add(entry)
    db.session.commit()
    flash(_('%(title)s added to %(day)s %(meal)s!', title=recipe.title, day=day, meal=meal_type), 'success')
    return redirect(url_for('planner.meal_planner'))



@planner.route('/meal-planner/remove/<int:entry_id>', methods=['POST'])
@login_required
def remove_from_plan(entry_id):
    entry = MealPlan.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash(_('Unauthorized.'), 'danger')
        return redirect(url_for('planner.meal_planner'))


    db.session.delete(entry)
    db.session.commit()
    flash(_('Recipe removed from plan.'), 'success')
    return redirect(url_for('planner.meal_planner'))



@planner.route('/meal-planner/clear', methods=['POST'])
@login_required
def clear_plan():
    MealPlan.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash(_('Meal plan cleared.'), 'success')
    return redirect(url_for('planner.meal_planner'))



@planner.route('/meal-planner/shopping-list')
@login_required
def shopping_list():
    meal_entries = MealPlan.query.filter_by(user_id=current_user.id).all()
    recipe_ids = list(set(e.recipe_id for e in meal_entries))
    recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()

    # Collect all ingredients grouped by name
    from collections import defaultdict
    ingredient_map = defaultdict(list)
    for recipe in recipes:
        for ing in recipe.ingredients:
            ingredient_map[ing.name.lower()].append({
                'quantity': ing.quantity,
                'unit': ing.unit,
                'recipe': recipe.title
            })

    return render_template('shopping_list.html',
                           ingredient_map=dict(ingredient_map),
                           recipes=recipes)
