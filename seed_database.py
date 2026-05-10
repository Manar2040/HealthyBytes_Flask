import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import db, create_app
from app.models import User, Category, Recipe, Review, Ingredient


def seed_database():
    print("Seeding database (EXTENDED FOR PANTRY CHEF)...")

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

    db.session.commit()

    # Extensive Database of 50 Recipes
    recipes_data = [
        # Original
        {"id": 1, "title": "Pancakes", "description": "Fluffy pancakes with maple syrup", "category_id": 1, "image_file": "pancakes.jpg", "calories": 290, "protein": 5, "carbs": 50, "fats": 8},
        {"id": 3, "title": "Omelette", "description": "Cheese and veggie omelette", "category_id": 1, "image_file": "omelette.jpg", "calories": 250, "protein": 18, "carbs": 2, "fats": 18},
        {"id": 4, "title": "Avocado Toast", "description": "Toasted bread topped with smashed avocado and poached egg", "category_id": 1, "image_file": "avocado_toast.jpg", "calories": 350, "protein": 8, "carbs": 30, "fats": 20},
        {"id": 5, "title": "French Toast", "description": "Golden brown French toast with cinnamon and syrup", "category_id": 1, "image_file": "french_toast.jpg", "calories": 350, "protein": 8, "carbs": 50, "fats": 12},
        {"id": 6, "title": "Smoothie Bowl", "description": "Mixed fruit smoothie topped with granola and fresh fruits", "category_id": 1, "image_file": "smoothie_bowl.jpg", "calories": 400, "protein": 15, "carbs": 60, "fats": 10},
        {"id": 7, "title": "Waffles", "description": "Crispy waffles served with fresh fruits and whipped cream", "category_id": 1, "image_file": "waffles.jpg", "calories": 300, "protein": 6, "carbs": 50, "fats": 10},
        {"id": 8, "title": "Grilled Chicken Salad", "description": "Fresh mixed greens topped with grilled chicken breast, cherry tomatoes, and vinaigrette.", "category_id": 2, "image_file": "grilled_chicken_salad.jpg", "calories": 350, "protein": 30, "carbs": 10, "fats": 15},
        {"id": 9, "title": "Beef Burger", "description": "Juicy beef patty served in a bun with cheese, lettuce, and special sauce", "category_id": 2, "image_file": "beef_burger.jpg", "calories": 500, "protein": 25, "carbs": 40, "fats": 28},
        {"id": 10, "title": "Spaghetti Bolognese", "description": "Classic Italian pasta with rich tomato and beef sauce", "category_id": 2, "image_file": "spaghetti_bolognese.jpg", "calories": 700, "protein": 35, "carbs": 80, "fats": 25},
        {"id": 11, "title": "Grilled Cheese Sandwich", "description": "Melted cheese between two slices of crispy toasted bread", "category_id": 2, "image_file": "grilled_cheese.jpg", "calories": 400, "protein": 15, "carbs": 40, "fats": 20},
        {"id": 12, "title": "Fish Tacos", "description": "Soft tortillas filled with crispy fish, slaw, and spicy mayo", "category_id": 2, "image_file": "fish_tacos.jpg", "calories": 300, "protein": 25, "carbs": 25, "fats": 12},
        {"id": 13, "title": "Tuna Melt", "description": "Toasted bread with tuna salad and melted cheddar cheese", "category_id": 2, "image_file": "tuna_melt.jpg", "calories": 450, "protein": 30, "carbs": 30, "fats": 25},
        {"id": 15, "title": "Eggplant Parmesan", "description": "Breaded eggplant layered with marinara and melted mozzarella", "category_id": 3, "image_file": "eggplant_parmesan.jpg", "calories": 400, "protein": 20, "carbs": 40, "fats": 18},
        {"id": 16, "title": "Shrimp Scampi Pasta", "description": "Garlicky shrimp tossed with linguine in white wine butter sauce", "category_id": 3, "image_file": "shrimp_scampi.jpg", "calories": 600, "protein": 35, "carbs": 50, "fats": 25},
        {"id": 17, "title": "Butternut Squash Soup", "description": "Velvety soup with roasted squash, sage, and a touch of cream", "category_id": 3, "image_file": "squash_soup.jpg", "calories": 200, "protein": 5, "carbs": 35, "fats": 5},
        {"id": 18, "title": "Lamb Kebabs", "description": "Marinated lamb grilled with bell peppers and onions", "category_id": 3, "image_file": "lamb_kebabs.jpg", "calories": 500, "protein": 35, "carbs": 2, "fats": 35},
        {"id": 19, "title": "Seafood Paella", "description": "Spanish rice dish with shrimp, mussels, and saffron", "category_id": 3, "image_file": "seafood_paella.jpg", "calories": 600, "protein": 30, "carbs": 65, "fats": 15},
        {"id": 20, "title": "Stuffed Bell Peppers", "description": "Peppers filled with ground turkey, rice, and tomatoes", "category_id": 3, "image_file": "stuffed_peppers.jpg", "calories": 350, "protein": 10, "carbs": 40, "fats": 12},
        {"id": 21, "title": "Molten Caramel Cake", "description": "Gooey caramel-filled cake with sea salt garnish", "category_id": 4, "image_file": "caramel_cake.jpg", "calories": 400, "protein": 5, "carbs": 50, "fats": 18},
        {"id": 22, "title": "Key Lime Pie", "description": "Tangy lime custard in graham cracker crust", "category_id": 4, "image_file": "key_lime_pie.jpg", "calories": 350, "protein": 6, "carbs": 50, "fats": 20},
        {"id": 24, "title": "Red Velvet Cake", "description": "Moist red cake with cream cheese frosting", "category_id": 4, "image_file": "red_velvet.jpg", "calories": 450, "protein": 6, "carbs": 60, "fats": 18},
        {"id": 25, "title": "Banana Pudding", "description": "Layered pudding with vanilla wafers and fresh bananas", "category_id": 4, "image_file": "banana_pudding.jpg", "calories": 300, "protein": 5, "carbs": 45, "fats": 10},
        {"id": 26, "title": "Lemon Tart", "description": "Buttery crust filled with tangy lemon curd", "category_id": 4, "image_file": "lemon_tart.jpg", "calories": 350, "protein": 5, "carbs": 50, "fats": 20},
        {"id": 27, "title": "Strawberry Cheesecake", "description": "Creamy cheesecake on graham crust with fresh strawberries", "category_id": 4, "image_file": "strawberry_cheesecake.jpg", "calories": 450, "protein": 8, "carbs": 50, "fats": 22},
        {"id": 28, "title": "Greek Yogurt Parfait", "description": "Greek yogurt layered with granola and fresh berries", "category_id": 1, "image_file": "Greek_Yogurt_Parfait.jpg", "calories": 250, "protein": 14, "carbs": 30, "fats": 4},
        {"id": 29, "title": "Oatmeal with Berries", "description": "Warm oatmeal served with mixed berries and honey", "category_id": 1, "image_file": "Oatmeal_with_Berries.jpg", "calories": 220, "protein": 6, "carbs": 40, "fats": 3},
        {"id": 30, "title": "Lentil Soup", "description": "Comforting and hearty lentil soup with spices", "category_id": 2, "image_file": "Lentil_Soup.jpg", "calories": 180, "protein": 12, "carbs": 25, "fats": 3},
        {"id": 31, "title": "Turkey Wraps", "description": "Healthy turkey wraps with veggies and low-fat dressing", "category_id": 2, "image_file": "Turkey_Wraps.jpg", "calories": 290, "protein": 24, "carbs": 30, "fats": 8},
        {"id": 32, "title": "Chicken Stir Fry", "description": "Quick chicken stir-fry with colorful veggies", "category_id": 3, "image_file": "Chicken_Stir_Fry.jpg", "calories": 350, "protein": 30, "carbs": 20, "fats": 12},
        {"id": 33, "title": "Zucchini Noodles with Pesto", "description": "Low-carb zucchini noodles tossed with fresh pesto", "category_id": 3, "image_file": "Zucchini_Noodles_with_Pesto.jpg", "calories": 320, "protein": 10, "carbs": 40, "fats": 10},
        {"id": 34, "title": "Frozen Yogurt Bites", "description": "Mini frozen yogurt bites with mixed fruits", "category_id": 4, "image_file": "Frozen_Yogurt_Bites.jpg", "calories": 100, "protein": 4, "carbs": 15, "fats": 2},
        {"id": 35, "title": "Chia Seed Pudding", "description": "Creamy chia pudding topped with fruits", "category_id": 4, "image_file": "Chia_Seed_Pudding.jpg", "calories": 180, "protein": 6, "carbs": 20, "fats": 8},
        # NEW RECIPES
        {"id": 36, "title": "Teriyaki Salmon", "description": "Glazed salmon fillets with homemade teriyaki sauce", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 420, "protein": 34, "carbs": 12, "fats": 22},
        {"id": 37, "title": "Quinoa Salad", "description": "Light and refreshing quinoa salad with cucumber and feta", "category_id": 2, "image_file": "default_recipe.jpg", "calories": 310, "protein": 12, "carbs": 38, "fats": 14},
        {"id": 38, "title": "Caesar Salad", "description": "Classic Caesar salad with homemade dressing and croutons", "category_id": 2, "image_file": "default_recipe.jpg", "calories": 350, "protein": 10, "carbs": 15, "fats": 28},
        {"id": 39, "title": "Vegetable Curry", "description": "Rich coconut milk vegetable curry with potatoes and carrots", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 380, "protein": 8, "carbs": 45, "fats": 20},
        {"id": 40, "title": "Mushroom Risotto", "description": "Creamy arborio rice with wild mushrooms and parmesan", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 450, "protein": 12, "carbs": 60, "fats": 18},
        {"id": 41, "title": "Protein Brownies", "description": "Fudgy chocolate brownies packed with whey protein", "category_id": 4, "image_file": "default_recipe.jpg", "calories": 200, "protein": 15, "carbs": 22, "fats": 8},
        {"id": 42, "title": "Shakshuka", "description": "Eggs poached in a sauce of tomatoes, chili peppers, and onions", "category_id": 1, "image_file": "default_recipe.jpg", "calories": 280, "protein": 14, "carbs": 20, "fats": 16},
        {"id": 43, "title": "Pesto Penne Pasta", "description": "Simple penne pasta tossed in basil pesto sauce", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 480, "protein": 12, "carbs": 65, "fats": 18},
        {"id": 44, "title": "Caprese Salad", "description": "Fresh mozzarella, tomatoes, and sweet basil", "category_id": 2, "image_file": "default_recipe.jpg", "calories": 250, "protein": 12, "carbs": 6, "fats": 18},
        {"id": 45, "title": "Baked Ziti", "description": "Cheesy baked ziti with marinara and ground sausage", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 550, "protein": 25, "carbs": 50, "fats": 26},
        {"id": 46, "title": "Minestrone Soup", "description": "Traditional Italian vegetable soup with beans and pasta", "category_id": 2, "image_file": "default_recipe.jpg", "calories": 200, "protein": 8, "carbs": 35, "fats": 4},
        {"id": 47, "title": "Mango Lassi", "description": "Refreshing Indian yogurt drink with fresh mango", "category_id": 4, "image_file": "default_recipe.jpg", "calories": 180, "protein": 6, "carbs": 32, "fats": 4},
        {"id": 48, "title": "BBQ Chicken Pizza", "description": "Homemade pizza topped with BBQ sauce, chicken, and red unions", "category_id": 3, "image_file": "default_recipe.jpg", "calories": 600, "protein": 35, "carbs": 70, "fats": 22},
        {"id": 49, "title": "Breakfast Burrito", "description": "Scrambled eggs, beans, and cheese wrapped in a tortilla", "category_id": 1, "image_file": "default_recipe.jpg", "calories": 450, "protein": 20, "carbs": 40, "fats": 25},
        {"id": 50, "title": "Fruit Salad", "description": "A mix of fresh seasonal fruits", "category_id": 1, "image_file": "default_recipe.jpg", "calories": 120, "protein": 1, "carbs": 30, "fats": 0},
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

    # Update recipe counts for each category
    for category in Category.query.all():
        category.recipes_count = Recipe.query.filter_by(category_id=category.id).count()

    db.session.commit()

    # Extensive Database of Ingredients for ALL 50 Recipes
    if Ingredient.query.count() == 0:
        ingredients_data = {
            1: [("All-purpose flour", "1.5", "cups"), ("Milk", "1.25", "cups"), ("Egg", "1", "large"), ("Butter", "3", "tbsp"), ("Sugar", "2", "tbsp"), ("Baking powder", "2", "tsp"), ("Salt", "0.5", "tsp"), ("Maple syrup", "4", "tbsp")],
            3: [("Eggs", "3", "large"), ("Cheddar cheese", "0.25", "cup"), ("Bell pepper", "0.25", "cup"), ("Onion", "2", "tbsp"), ("Mushrooms", "0.25", "cup"), ("Salt", "0.25", "tsp"), ("Pepper", "0.25", "tsp"), ("Butter", "1", "tbsp")],
            4: [("Sourdough bread", "2", "slices"), ("Avocado", "1", "ripe"), ("Egg", "1", "large"), ("Cherry tomatoes", "4", "pieces"), ("Red pepper flakes", "0.25", "tsp"), ("Lemon juice", "1", "tsp"), ("Salt", "0.25", "tsp")],
            5: [("Bread", "4", "slices"), ("Eggs", "2", "large"), ("Milk", "0.5", "cup"), ("Cinnamon", "1", "tsp"), ("Vanilla extract", "1", "tsp"), ("Butter", "2", "tbsp"), ("Maple syrup", "2", "tbsp")],
            6: [("Banana", "1", "frozen"), ("Mixed berries", "1", "cup"), ("Almond milk", "0.5", "cup"), ("Granola", "0.25", "cup"), ("Chia seeds", "1", "tbsp"), ("Honey", "1", "tsp")],
            7: [("All-purpose flour", "2", "cups"), ("Milk", "1.5", "cups"), ("Eggs", "2", "large"), ("Vegetable oil", "0.5", "cup"), ("Sugar", "1", "tbsp"), ("Baking powder", "4", "tsp"), ("Salt", "0.25", "tsp")],
            8: [("Chicken breast", "200", "g"), ("Mixed salad greens", "3", "cups"), ("Cherry tomatoes", "0.5", "cup"), ("Cucumber", "0.5", "medium"), ("Red onion", "0.25", "medium"), ("Olive oil", "2", "tbsp"), ("Balsamic vinegar", "1", "tbsp"), ("Salt", "0.5", "tsp"), ("Black pepper", "0.25", "tsp")],
            9: [("Ground beef", "200", "g"), ("Hamburger bun", "1", "piece"), ("Cheddar cheese", "1", "slice"), ("Lettuce", "1", "leaf"), ("Tomato", "1", "slice"), ("Onion", "1", "slice"), ("Ketchup", "1", "tbsp")],
            10: [("Spaghetti", "400", "g"), ("Ground beef", "500", "g"), ("Onion", "1", "large"), ("Garlic", "3", "cloves"), ("Tomato sauce", "2", "cups"), ("Tomato paste", "2", "tbsp"), ("Olive oil", "2", "tbsp"), ("Oregano", "1", "tsp"), ("Basil", "1", "tsp"), ("Salt", "1", "tsp"), ("Parmesan cheese", "0.25", "cup")],
            11: [("Bread", "2", "slices"), ("Cheddar cheese", "2", "slices"), ("Butter", "1", "tbsp")],
            12: [("White fish fillets", "300", "g"), ("Corn tortillas", "4", "pieces"), ("Cabbage slaw", "1", "cup"), ("Spicy mayo", "2", "tbsp"), ("Lime", "1", "piece"), ("Cilantro", "2", "tbsp")],
            13: [("Bread", "2", "slices"), ("Canned tuna", "1", "can"), ("Mayonnaise", "2", "tbsp"), ("Cheddar cheese", "2", "slices"), ("Celery", "1", "stalk"), ("Butter", "1", "tbsp")],
            15: [("Eggplant", "1", "large"), ("Marinara sauce", "2", "cups"), ("Mozzarella cheese", "1", "cup"), ("Parmesan cheese", "0.5", "cup"), ("Breadcrumbs", "1", "cup"), ("Eggs", "2", "large"), ("Olive oil", "2", "tbsp")],
            16: [("Linguine", "350", "g"), ("Shrimp", "500", "g"), ("Garlic", "4", "cloves"), ("White wine", "0.5", "cup"), ("Butter", "3", "tbsp"), ("Olive oil", "2", "tbsp"), ("Lemon juice", "2", "tbsp"), ("Red pepper flakes", "0.25", "tsp"), ("Parsley", "2", "tbsp"), ("Salt", "0.5", "tsp")],
            17: [("Butternut squash", "1", "large"), ("Onion", "1", "medium"), ("Garlic", "2", "cloves"), ("Vegetable broth", "3", "cups"), ("Heavy cream", "0.25", "cup"), ("Sage", "1", "tsp"), ("Olive oil", "2", "tbsp"), ("Salt", "0.5", "tsp"), ("Nutmeg", "0.25", "tsp")],
            18: [("Lamb meat", "500", "g"), ("Bell pepper", "2", "medium"), ("Red onion", "1", "large"), ("Olive oil", "2", "tbsp"), ("Garlic", "2", "cloves"), ("Cumin", "1", "tsp"), ("Coriander", "1", "tsp")],
            19: [("Arborio rice", "1.5", "cups"), ("Shrimp", "250", "g"), ("Mussels", "250", "g"), ("Chicken broth", "3", "cups"), ("Saffron", "1", "pinch"), ("Bell pepper", "1", "medium"), ("Onion", "1", "medium"), ("Garlic", "2", "cloves"), ("Olive oil", "2", "tbsp")],
            20: [("Bell pepper", "4", "large"), ("Ground turkey", "400", "g"), ("Cooked rice", "1", "cup"), ("Tomato sauce", "1", "cup"), ("Onion", "1", "medium"), ("Garlic", "2", "cloves"), ("Mozzarella cheese", "0.5", "cup")],
            21: [("Dark chocolate", "100", "g"), ("Butter", "100", "g"), ("Eggs", "2", "large"), ("Sugar", "0.5", "cup"), ("All-purpose flour", "2", "tbsp"), ("Caramel sauce", "4", "tbsp"), ("Sea salt", "0.25", "tsp")],
            22: [("Graham cracker crumbs", "1.5", "cups"), ("Butter", "5", "tbsp"), ("Sweetened condensed milk", "1", "can"), ("Key lime juice", "0.5", "cup"), ("Egg yolks", "4", "large")],
            24: [("All-purpose flour", "2.5", "cups"), ("Sugar", "1.5", "cups"), ("Cocoa powder", "2", "tbsp"), ("Baking soda", "1", "tsp"), ("Salt", "1", "tsp"), ("Eggs", "2", "large"), ("Vegetable oil", "1", "cup"), ("Buttermilk", "1", "cup"), ("Red food coloring", "2", "tbsp"), ("Cream cheese", "8", "oz")],
            25: [("Vanilla wafers", "1", "box"), ("Bananas", "4", "medium"), ("Milk", "2", "cups"), ("Vanilla pudding mix", "1", "box"), ("Sweetened condensed milk", "1", "can"), ("Heavy cream", "1", "cup")],
            26: [("Pie crust", "1", "piece"), ("Lemons", "4", "medium"), ("Sugar", "1", "cup"), ("Eggs", "4", "large"), ("Butter", "0.5", "cup")],
            27: [("Cream cheese", "16", "oz"), ("Sugar", "0.75", "cup"), ("Vanilla extract", "1", "tsp"), ("Eggs", "2", "large"), ("Graham cracker crust", "1", "piece"), ("Strawberries", "1", "cup")],
            28: [("Greek yogurt", "1", "cup"), ("Granola", "0.5", "cup"), ("Blueberries", "0.25", "cup"), ("Strawberries", "0.25", "cup"), ("Honey", "1", "tbsp")],
            29: [("Rolled oats", "0.5", "cup"), ("Milk", "1", "cup"), ("Mixed berries", "0.5", "cup"), ("Honey", "1", "tbsp")],
            30: [("Red lentils", "1", "cup"), ("Onion", "1", "medium"), ("Carrot", "2", "medium"), ("Celery", "2", "stalks"), ("Garlic", "3", "cloves"), ("Cumin", "1", "tsp"), ("Vegetable broth", "4", "cups"), ("Olive oil", "2", "tbsp"), ("Lemon juice", "1", "tbsp"), ("Salt", "1", "tsp")],
            31: [("Tortilla wrap", "2", "pieces"), ("Turkey slices", "150", "g"), ("Lettuce", "1", "cup"), ("Tomato", "1", "medium"), ("Mayonnaise", "1", "tbsp")],
            32: [("Chicken breast", "300", "g"), ("Broccoli", "1", "cup"), ("Bell peppers", "1", "cup"), ("Carrot", "1", "medium"), ("Soy sauce", "3", "tbsp"), ("Sesame oil", "1", "tbsp"), ("Garlic", "2", "cloves"), ("Ginger", "1", "tsp"), ("Cornstarch", "1", "tbsp"), ("Vegetable oil", "2", "tbsp")],
            33: [("Zucchini", "2", "medium"), ("Pesto sauce", "0.25", "cup"), ("Cherry tomatoes", "0.5", "cup"), ("Parmesan cheese", "2", "tbsp")],
            34: [("Greek yogurt", "1", "cup"), ("Honey", "2", "tbsp"), ("Mixed berries", "0.5", "cup")],
            35: [("Chia seeds", "0.25", "cup"), ("Almond milk", "1", "cup"), ("Honey", "1", "tbsp"), ("Vanilla extract", "0.5", "tsp")],
            36: [("Salmon fillet", "2", "pieces"), ("Soy sauce", "2", "tbsp"), ("Brown sugar", "1", "tbsp"), ("Ginger", "1", "tsp"), ("Garlic", "1", "clove"), ("Sesame seeds", "1", "tsp")],
            37: [("Quinoa", "1", "cup"), ("Cucumber", "1", "medium"), ("Cherry tomatoes", "1", "cup"), ("Red onion", "0.25", "medium"), ("Feta cheese", "0.5", "cup"), ("Olive oil", "2", "tbsp"), ("Lemon juice", "2", "tbsp")],
            38: [("Romaine lettuce", "1", "head"), ("Croutons", "1", "cup"), ("Parmesan cheese", "0.5", "cup"), ("Caesar dressing", "0.25", "cup"), ("Chicken breast", "1", "piece")],
            39: [("Coconut milk", "1", "can"), ("Curry paste", "2", "tbsp"), ("Potatoes", "2", "medium"), ("Carrot", "2", "medium"), ("Broccoli", "1", "cup"), ("Vegetable broth", "1", "cup"), ("Olive oil", "1", "tbsp")],
            40: [("Arborio rice", "1", "cup"), ("Wild mushrooms", "200", "g"), ("Vegetable broth", "4", "cups"), ("White wine", "0.5", "cup"), ("Onion", "1", "medium"), ("Parmesan cheese", "0.5", "cup"), ("Butter", "2", "tbsp"), ("Olive oil", "1", "tbsp")],
            41: [("Whey protein powder", "2", "scoops"), ("Cocoa powder", "0.25", "cup"), ("Almond flour", "0.5", "cup"), ("Eggs", "2", "large"), ("Almond milk", "0.5", "cup"), ("Dark chocolate chips", "0.25", "cup")],
            42: [("Eggs", "4", "large"), ("Tomato sauce", "2", "cups"), ("Bell pepper", "1", "medium"), ("Onion", "1", "medium"), ("Garlic", "2", "cloves"), ("Cumin", "1", "tsp"), ("Paprika", "1", "tsp"), ("Olive oil", "2", "tbsp")],
            43: [("Penne pasta", "400", "g"), ("Pesto sauce", "0.5", "cup"), ("Parmesan cheese", "0.25", "cup"), ("Pine nuts", "2", "tbsp"), ("Olive oil", "1", "tbsp")],
            44: [("Fresh mozzarella", "200", "g"), ("Tomatoes", "3", "medium"), ("Fresh basil", "1", "handful"), ("Olive oil", "2", "tbsp"), ("Balsamic glaze", "1", "tbsp"), ("Salt", "0.25", "tsp")],
            45: [("Ziti pasta", "400", "g"), ("Marinara sauce", "3", "cups"), ("Ground sausage", "300", "g"), ("Ricotta cheese", "1", "cup"), ("Mozzarella cheese", "2", "cups"), ("Parmesan cheese", "0.5", "cup")],
            46: [("Vegetable broth", "4", "cups"), ("Diced tomatoes", "1", "can"), ("Kidney beans", "1", "can"), ("Small pasta", "0.5", "cup"), ("Carrot", "1", "medium"), ("Celery", "1", "stalk"), ("Onion", "1", "medium"), ("Italian seasoning", "1", "tsp")],
            47: [("Mango", "1", "ripe"), ("Yogurt", "1", "cup"), ("Milk", "0.5", "cup"), ("Sugar", "1", "tbsp"), ("Cardamom", "1", "pinch")],
            48: [("Pizza dough", "1", "piece"), ("BBQ sauce", "0.5", "cup"), ("Cooked chicken", "1", "cup"), ("Red onion", "0.5", "medium"), ("Mozzarella cheese", "1.5", "cups"), ("Cilantro", "2", "tbsp")],
            49: [("Tortilla wrap", "2", "large"), ("Eggs", "4", "large"), ("Black beans", "0.5", "cup"), ("Cheddar cheese", "0.5", "cup"), ("Salsa", "2", "tbsp"), ("Butter", "1", "tbsp")],
            50: [("Strawberries", "1", "cup"), ("Grapes", "1", "cup"), ("Blueberries", "0.5", "cup"), ("Apple", "1", "medium"), ("Orange", "1", "medium"), ("Honey", "1", "tbsp")]
        }

        for recipe_id, ingredients in ingredients_data.items():
            for name, quantity, unit in ingredients:
                ingredient = Ingredient(
                    name=name,
                    quantity=quantity,
                    unit=unit,
                    recipe_id=recipe_id
                )
                db.session.add(ingredient)

        # Let's also add dummy reviews for everyone so ratings work
        print("Seeding reviews...")
        import random
        users = User.query.all()
        for i in range(1, 51):
            for _ in range(random.randint(1, 4)):
                rev = Review(
                    rating=random.randint(3, 5),
                    content="Great recipe! Highly recommended.",
                    user_id=users[0].id,
                    recipe_id=i
                )
                db.session.add(rev)

        db.session.commit()

    print("Database seeding completed!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()