import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, bcrypt, db, mail
from app.forms import LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ContentForm
from app.models import User, Content
from flask_login import login_user , current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    content = Content.query.first()
    return render_template('index.html', content=content)

@app.route("/content")
def content():
    c = Content.query.first()
    con = {}
    con['inv'] = c.inv_content
    con['adv'] = c.adv_content
    con['bey'] = c.bey_content
    con['net'] = c.net_content
    con['mor'] = c.mor_content
    return jsonify(con)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Unsuccessful login. Please check Email and Password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='img/profile/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/update_content", methods=['GET', 'POST'])
@login_required
def update_content():
    form = ContentForm()
    if form.validate_on_submit():
        content = Content.query.first()
        if form.invskills.data:
            content.inv_content = form.invskills.data
        if form.advitex.data:
            content.adv_content = form.advitex.data
        if form.beyondclick.data:
            content.bey_content = form.beyondclick.data
        if form.nanonet.data:
            content.net_content = form.nanonet.data
        if form.moroorgar.data:
            content.mor_content = form.moroorgar.data
        if form.email.data:
            content.inv_email = form.email.data
        if form.address.data:
            content.inv_address = form.address.data
        if form.phone.data:
            content.inv_phone = form.phone.data
        db.session.commit()
        flash('Your web site has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template('update_content.html', title='Update Content', form=form)
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500