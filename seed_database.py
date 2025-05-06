import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import db, create_app
from app.models import User, Category, Recipe, Review


def seed_database():
    """
    Seeds the database with initial data for categories and recipes
    and connects the nutritional info from the SQL data
    """
    print("Seeding database...")

    # Create admin user
    admin_user = User.query.filter_by(email="admin@healthybytes.com").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@healthybytes.com",
            password=generate_password_hash("adminpassword")
        )
        db.session.add(admin_user)
        print("Added admin user")

    # Create categories
    categories_data = [
        {"id": 1, "name": "Breakfast", "description": "Start your day with these nutritious breakfast recipes"},
        {"id": 2, "name": "Lunch", "description": "Healthy and satisfying midday meal options"},
        {"id": 3, "name": "Dinner", "description": "Nutritious dinner recipes to end your day right"},
        {"id": 4, "name": "Dessert", "description": "Healthier versions of your favorite sweet treats"}
    ]

    for cat_data in categories_data:
        category = Category.query.get(cat_data["id"])
        if not category:
            category = Category(
                id=cat_data["id"],
                name=cat_data["name"],
                description=cat_data["description"]
            )
            db.session.add(category)
            print(f"Added category: {cat_data['name']}")

    db.session.commit()

    # Recipe data (combining both recipes and nutritional info from your SQL)
    recipes_data = [
        {"id": 1, "title": "Pancakes", "description": "Fluffy pancakes with maple syrup", "category_id": 1,
         "image_file": "pancakes.jpg", "calories": 290, "protein": 5, "carbs": 50, "fats": 8},
        {"id": 3, "title": "Omelette", "description": "Cheese and veggie omelette", "category_id": 1,
         "image_file": "omelette.jpg", "calories": 250, "protein": 18, "carbs": 2, "fats": 18},
        {"id": 4, "title": "Avocado Toast", "description": "Toasted bread topped with smashed avocado and poached egg",
         "category_id": 1, "image_file": "avocado_toast.jpg", "calories": 350, "protein": 8, "carbs": 30, "fats": 20},
        {"id": 5, "title": "French Toast", "description": "Golden brown French toast with cinnamon and syrup",
         "category_id": 1, "image_file": "french_toast.jpg", "calories": 350, "protein": 8, "carbs": 50, "fats": 12},
        {"id": 6, "title": "Smoothie Bowl", "description": "Mixed fruit smoothie topped with granola and fresh fruits",
         "category_id": 1, "image_file": "smoothie_bowl.jpg", "calories": 400, "protein": 15, "carbs": 60, "fats": 10},
        {"id": 7, "title": "Waffles", "description": "Crispy waffles served with fresh fruits and whipped cream",
         "category_id": 1, "image_file": "waffles.jpg", "calories": 300, "protein": 6, "carbs": 50, "fats": 10},
        {"id": 8, "title": "Grilled Chicken Salad",
         "description": "Fresh mixed greens topped with grilled chicken breast, cherry tomatoes, and vinaigrette.",
         "category_id": 2, "image_file": "grilled_chicken_salad.jpg", "calories": 350, "protein": 30, "carbs": 10,
         "fats": 15},
        {"id": 9, "title": "Beef Burger",
         "description": "Juicy beef patty served in a bun with cheese, lettuce, and special sauce", "category_id": 2,
         "image_file": "beef_burger.jpg", "calories": 500, "protein": 25, "carbs": 40, "fats": 28},
        {"id": 10, "title": "Spaghetti Bolognese",
         "description": "Classic Italian pasta with rich tomato and beef sauce", "category_id": 2,
         "image_file": "spaghetti_bolognese.jpg", "calories": 700, "protein": 35, "carbs": 80, "fats": 25},
        {"id": 11, "title": "Grilled Cheese Sandwich",
         "description": "Melted cheese between two slices of crispy toasted bread", "category_id": 2,
         "image_file": "grilled_cheese.jpg", "calories": 400, "protein": 15, "carbs": 40, "fats": 20},
        {"id": 12, "title": "Fish Tacos", "description": "Soft tortillas filled with crispy fish, slaw, and spicy mayo",
         "category_id": 2, "image_file": "fish_tacos.jpg", "calories": 300, "protein": 25, "carbs": 25, "fats": 12},
        {"id": 13, "title": "Tuna Melt", "description": "Toasted bread with tuna salad and melted cheddar cheese",
         "category_id": 2, "image_file": "tuna_melt.jpg", "calories": 450, "protein": 30, "carbs": 30, "fats": 25},
        {"id": 15, "title": "Eggplant Parmesan",
         "description": "Breaded eggplant layered with marinara and melted mozzarella", "category_id": 3,
         "image_file": "eggplant_parmesan.jpg", "calories": 400, "protein": 20, "carbs": 40, "fats": 18},
        {"id": 16, "title": "Shrimp Scampi Pasta",
         "description": "Garlicky shrimp tossed with linguine in white wine butter sauce", "category_id": 3,
         "image_file": "shrimp_scampi.jpg", "calories": 600, "protein": 35, "carbs": 50, "fats": 25},
        {"id": 17, "title": "Butternut Squash Soup",
         "description": "Velvety soup with roasted squash, sage, and a touch of cream", "category_id": 3,
         "image_file": "squash_soup.jpg", "calories": 200, "protein": 5, "carbs": 35, "fats": 5},
        {"id": 18, "title": "Lamb Kebabs", "description": "Marinated lamb grilled with bell peppers and onions",
         "category_id": 3, "image_file": "lamb_kebabs.jpg", "calories": 500, "protein": 35, "carbs": 2, "fats": 35},
        {"id": 19, "title": "Seafood Paella", "description": "Spanish rice dish with shrimp, mussels, and saffron",
         "category_id": 3, "image_file": "seafood_paella.jpg", "calories": 600, "protein": 30, "carbs": 65, "fats": 15},
        {"id": 20, "title": "Stuffed Bell Peppers",
         "description": "Peppers filled with ground turkey, rice, and tomatoes", "category_id": 3,
         "image_file": "stuffed_peppers.jpg", "calories": 350, "protein": 10, "carbs": 40, "fats": 12},
        {"id": 21, "title": "Molten Caramel Cake", "description": "Gooey caramel-filled cake with sea salt garnish",
         "category_id": 4, "image_file": "caramel_cake.jpg", "calories": 400, "protein": 5, "carbs": 50, "fats": 18},
        {"id": 22, "title": "Key Lime Pie", "description": "Tangy lime custard in graham cracker crust",
         "category_id": 4, "image_file": "key_lime_pie.jpg", "calories": 350, "protein": 6, "carbs": 50, "fats": 20},
        {"id": 24, "title": "Red Velvet Cake", "description": "Moist red cake with cream cheese frosting",
         "category_id": 4, "image_file": "red_velvet.jpg", "calories": 450, "protein": 6, "carbs": 60, "fats": 18},
        {"id": 25, "title": "Banana Pudding", "description": "Layered pudding with vanilla wafers and fresh bananas",
         "category_id": 4, "image_file": "banana_pudding.jpg", "calories": 300, "protein": 5, "carbs": 45, "fats": 10},
        {"id": 26, "title": "Lemon Tart", "description": "Buttery crust filled with tangy lemon curd", "category_id": 4,
         "image_file": "lemon_tart.jpg", "calories": 350, "protein": 5, "carbs": 50, "fats": 20},
        {"id": 27, "title": "Strawberry Cheesecake",
         "description": "Creamy cheesecake on graham crust with fresh strawberries", "category_id": 4,
         "image_file": "strawberry_cheesecake.jpg", "calories": 450, "protein": 8, "carbs": 50, "fats": 22},
        {"id": 28, "title": "Greek Yogurt Parfait",
         "description": "Greek yogurt layered with granola and fresh berries", "category_id": 1,
         "image_file": "Greek_Yogurt_Parfait.jpg", "calories": 250, "protein": 14, "carbs": 30, "fats": 4},
        {"id": 29, "title": "Oatmeal with Berries", "description": "Warm oatmeal served with mixed berries and honey",
         "category_id": 1, "image_file": "Oatmeal_with_Berries.jpg", "calories": 220, "protein": 6, "carbs": 40,
         "fats": 3},
        {"id": 30, "title": "Lentil Soup", "description": "Comforting and hearty lentil soup with spices",
         "category_id": 2, "image_file": "Lentil_Soup.jpg", "calories": 180, "protein": 12, "carbs": 25, "fats": 3},
        {"id": 31, "title": "Turkey Wraps", "description": "Healthy turkey wraps with veggies and low-fat dressing",
         "category_id": 2, "image_file": "Turkey_Wraps.jpg", "calories": 290, "protein": 24, "carbs": 30, "fats": 8},
        {"id": 32, "title": "Chicken Stir Fry", "description": "Quick chicken stir-fry with colorful veggies",
         "category_id": 3, "image_file": "Chicken_Stir_Fry.jpg", "calories": 350, "protein": 30, "carbs": 20,
         "fats": 12},
        {"id": 33, "title": "Zucchini Noodles with Pesto",
         "description": "Low-carb zucchini noodles tossed with fresh pesto", "category_id": 3,
         "image_file": "Zucchini_Noodles_with_Pesto.jpg", "calories": 320, "protein": 10, "carbs": 40, "fats": 10},
        {"id": 34, "title": "Frozen Yogurt Bites", "description": "Mini frozen yogurt bites with mixed fruits",
         "category_id": 4, "image_file": "Frozen_Yogurt_Bites.jpg", "calories": 100, "protein": 4, "carbs": 15,
         "fats": 2},
        {"id": 35, "title": "Chia Seed Pudding", "description": "Creamy chia pudding topped with fruits",
         "category_id": 4, "image_file": "Chia_Seed_Pudding.jpg", "calories": 180, "protein": 6, "carbs": 20, "fats": 8}
    ]

    for recipe_data in recipes_data:
        recipe = Recipe.query.get(recipe_data["id"])
        if not recipe:
            recipe = Recipe(
                id=recipe_data["id"],
                title=recipe_data["title"],
                description=recipe_data["description"],
                calories=recipe_data["calories"],
                protein=recipe_data["protein"],
                carbs=recipe_data["carbs"],
                fats=recipe_data["fats"],
                image_file=recipe_data["image_file"],
                category_id=recipe_data["category_id"]
            )
            db.session.add(recipe)
            print(f"Added recipe: {recipe_data['title']}")

    # Update recipe counts for each category
    for category in Category.query.all():
        category.recipes_count = Recipe.query.filter_by(category_id=category.id).count()

    # Add some sample reviews
    if Review.query.count() == 0:
        sample_reviews = [
            {"recipe_id": 1, "user_id": 1, "rating": 5, "content": "Perfect pancakes! So fluffy and delicious."},
            {"recipe_id": 8, "user_id": 1, "rating": 4,
             "content": "The grilled chicken salad was fresh and satisfying."},
            {"recipe_id": 16, "user_id": 1, "rating": 5, "content": "This shrimp scampi is restaurant quality!"},
            {"recipe_id": 21, "user_id": 1, "rating": 4, "content": "Decadent but worth every calorie."}
        ]

        for review_data in sample_reviews:
            review = Review(
                recipe_id=review_data["recipe_id"],
                user_id=review_data["user_id"],
                rating=review_data["rating"],
                content=review_data["content"],
                date_posted=datetime.utcnow()
            )
            db.session.add(review)
            print(f"Added review for recipe ID: {review_data['recipe_id']}")

    db.session.commit()
    print("Database seeding completed!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()