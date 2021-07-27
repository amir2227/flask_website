from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Content
from flask_login import login_user , current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashbord'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashbord'))
        else:
            flash('Unsuccessful login. Please check Email and Password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='img/profile/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)