from flask import render_template
from . import auth
from .forms import LoginForm, RegistrationForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', title='Log In', form=form)

@auth.route('/register')
def register():
    form = RegistrationForm()
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/logout')
def logout():
    return render_template('auth/logout.html')
