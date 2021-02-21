from flask import render_template,request, current_app, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from .forms import LoginForm, RegistrationForm

from . import auth_bp
from app.models import User
from app import db, login


@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_dir.index'))

    form = LoginForm()
    username = form.username.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_dir.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            current_app.logger.debug('logged as %s' , username)
            return redirect(url_for('main_dir.index', username=username))
        return redirect(next_page)
    return render_template('auth/login.html',title='Log In', form=form)


@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_dir.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth_dir.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_dir.index'))


@auth_bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

