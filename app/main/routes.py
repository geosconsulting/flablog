from flask import render_template
from . import main

@main.route('/')
@main.route('/home')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    return render_template('main/about.html')
