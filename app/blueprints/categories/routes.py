from app.blueprints.categories import categories

@categories.route('/')
def all_categories():
    return "All categories"  # Placeholder

@categories.route('/<int:category_id>')
def recipes_by_category(category_id):
    return f"Recipes in category {category_id}"  # Placeholder