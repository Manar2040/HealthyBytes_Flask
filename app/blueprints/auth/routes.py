from app.blueprints.auth import auth

@auth.route('/login')
def login():
    return "Login page"  # Placeholder

@auth.route('/register')
def register():
    return "Register page"  # Placeholder

@auth.route('/profile')
def profile():
    return "Profile page"  # Placeholder