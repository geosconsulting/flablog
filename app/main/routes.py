from flask import render_template,request, flash
from . import main

@main.route('/')
@main.route('/home')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    flash(u'Invalid password provided', 'error')
    return render_template('main/about.html')
#
# @main.route('/select_test')
# def select_test():
#     return render_template('main/select_send.html')
#
# @main.route("/test" , methods=['GET', 'POST'])
# def test():
#     select = request.form.get('sel1')
#     return(str(select)) # just to see what select is
