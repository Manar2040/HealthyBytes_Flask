from app.blueprints.recipes import recipes

@recipes.route('/')
def all_recipes():
    return "All recipes"  # Placeholder

@recipes.route('/<int:recipe_id>')
def recipe_detail(recipe_id):
    return f"Recipe {recipe_id} details"  # Placeholder