from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class ContentForm(FlaskForm):
    invskills = TextAreaField('InvSkills Content' )
    advitex = TextAreaField('Advitex Content')
    beyondclick = TextAreaField('BeyondClick Content')
    nanonet = TextAreaField('NanoNet Content')
    moroorgar = TextAreaField('Moroorgar Content')
    email = StringField('InvEmail', validators=[Email()])
    address = StringField('Address')
    phone = StringField('Phone Number')
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateLogoForm(FlaskForm):
    inv_logo = FileField('Update Investing Skills Logo', validators=[FileAllowed(['jpg', 'png'])])
    adv_logo = FileField('Update Advitex Logo', validators=[FileAllowed(['jpg', 'png'])])
    bey_logo = FileField('Update Beyond Click Logo', validators=[FileAllowed(['jpg', 'png'])])
    net_logo = FileField('Update Nano Net Logo', validators=[FileAllowed(['jpg', 'png'])])
    mor_logo = FileField('Update Moroorgar Logo', validators=[FileAllowed(['jpg', 'png'])])
    about_pic = FileField('Update About Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')