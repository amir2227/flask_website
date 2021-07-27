from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Content


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@invskills.com' and form.password.data == 'admin':
            flash('you loged in successfully', 'success')
            return redirect(url_for('dashbord'))
        else:
            flash('Unsuccessful login. Please check Email and Password.', 'danger')
    return render_template('login.html', title='Login', form=form)
