from flask import render_template, flash, redirect, abort, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import Sotrudnik

@app.route('/')
@app.route ('/index')
def index():
    user = {'nickname' : 'Mishanya'}
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
#?    if g.user is not None and g.user.is_authenticated:
#?        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Sotrudnik.query.filter_by(email=form.login.data).first()


        if user is not None and user.verify_password(form.password.data):
            print(user.nickname)
            print(type(user.nickname))
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or/and password')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out')
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return Sotrudnik.query.get(int(id))


