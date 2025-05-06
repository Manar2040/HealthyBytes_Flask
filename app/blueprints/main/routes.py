from flask import render_template
from app.models import Recipe, Category
from app.blueprints.main import main

@main.route('/')
@main.route('/home')
def home():

    return render_template('home.html', )

@main.route('/about')
def about():
    return render_template('about.html', title='About Us')