from flask import render_template
from app.blueprints.main import main

@main.route('/')
@main.route('/home')
def home():
    return "Hello, World!"  # Placeholder

@main.route('/about')
def about():
    return "About page"  # Placeholder