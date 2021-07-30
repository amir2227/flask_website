from types import MethodType
from typing import Any
from flask import render_template, url_for, flash, redirect, request, jsonify
from werkzeug.utils import validate_arguments
from wtforms.validators import Email
from app import app, bcrypt, db
from app.forms import (LoginForm, UpdateAccountForm, RequestResetForm,
                    ResetPasswordForm, ContentForm, UpdateLogoForm, ContactForm)
from app.models import User, Content, Picture
from app.utils import save_logo, save_picture, send_reset_email, send_contact_email
from flask_login import login_user , current_user, logout_user, login_required


@app.route("/", methods=['POST', 'GET'])
@app.route("/home")
def home():
    content = Content.query.first()
    pic = Picture.query.first()
    pics = {'inv': url_for('static', filename='img/'+ pic.inv_logo),
            'adv': url_for('static', filename='img/'+ pic.adv_logo),
            'bey': url_for('static', filename='img/'+ pic.bey_logo),
            'net': url_for('static', filename='img/'+ pic.net_logo),
            'mor': url_for('static', filename='img/'+ pic.mor_logo),
            'about': url_for('static', filename='img/'+ pic.about_pic)}
    form = ContactForm()
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        message = form.message.data
        send_contact_email(name=name, email=email, message=message)
    return render_template('index.html', content=content, logo=pics, form=form)

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

@app.route("/update_logo", methods=['GET', 'POST'])
@login_required
def update_logo():
    form = UpdateLogoForm()
    logo = Picture.query.first()
    if form.validate_on_submit():
        if form.inv_logo.data:
            picture_file = save_logo(form.inv_logo.data)
            logo.inv_logo = picture_file
        if form.adv_logo.data:
            picture_file = save_logo(form.adv_logo.data)
            logo.adv_logo = picture_file
        if form.bey_logo.data:
            picture_file = save_logo(form.bey_logo.data)
            logo.bey_logo = picture_file
        if form.net_logo.data:
            picture_file = save_logo(form.net_logo.data)
            logo.net_logo = picture_file
        if form.mor_logo.data:
            picture_file = save_logo(form.mor_logo.data)
            logo.mor_logo = picture_file
        if form.about_pic.data:
            picture_file = save_logo(form.about_pic.data)
            logo.about_pic = picture_file
        db.session.commit()
        flash('Your website has been updated!', 'success')
        return redirect(url_for('update_logo'))
    pics = {'inv': url_for('static', filename='img/'+ logo.inv_logo),
            'adv': url_for('static', filename='img/'+ logo.adv_logo),
            'bey': url_for('static', filename='img/'+ logo.bey_logo),
            'net': url_for('static', filename='img/'+ logo.net_logo),
            'mor': url_for('static', filename='img/'+ logo.mor_logo),
            'about': url_for('static', filename='img/'+ logo.about_pic)}
    
    return render_template('update_pics.html', title='Update Pictures', logo=pics, form=form)


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
        return redirect(url_for('update_content'))
    return render_template('update_content.html', title='Update Content', form=form)

@app.route("/send_mail", methods=['POST'])
def send_mail():
    form = ContactForm()
    if form.validate_on_submit():
        print(form.email.data)

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500