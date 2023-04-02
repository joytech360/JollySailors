from base64 import b64encode
import jwt
from string import punctuation
from sqlalchemy import func

from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, HiddenField, IntegerField, TimeField, FileField, DateField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Email, EqualTo

from app.models import User


def validate_select(form, field):
    if field.data == 0:
        raise ValidationError("Please select from choice list")


class RegistrationForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'autocomplete': 'off'})
    # area = SelectField('Area', coerce=int, validators=[DataRequired(), validate_select])
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={'autocomplete': 'off'})
    submit = SubmitField('Register', render_kw={'class': 'btn btn-primary mt-2'})

    def validate_email(self, email):
        user = User.query.filter(func.lower(User.email) == email.data.lower().replace(' ', '')).first()
        if user is not None:
            raise ValidationError('Email is already registered!')

    def validate_password(self, password):
        passwd = password.data
        spec_char = set(punctuation)

        if len(passwd) < 8:
            raise ValidationError('Password length should be at least 8 characters!')

        if len(passwd) > 50:
            raise ValidationError('Password length should be greater than 50 characters!')

        if not any(char.isdigit() for char in passwd):
            raise ValidationError('Password should have at least one number!')

        if not any(char.isupper() for char in passwd):
            raise ValidationError('Password should have at least one uppercase letter!')

        if not any(char.islower() for char in passwd):
            raise ValidationError('Password should have at least one lowercase letter!')

        if not any(char in spec_char for char in passwd):
            raise ValidationError('Password should have at least one special character!')



class AdminApplyForm(FlaskForm):
    name = StringField('Daycare name', validators=[DataRequired()])
    submit = SubmitField('Apply', render_kw={'class': 'btn btn-primary mt-2'})


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={'autocomplete': 'off'})
    submit = SubmitField('Submit', render_kwargs={'class': 'btn btn-primary m-2'})

    def __init__(self, user, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_password(self, password):
        passwd = password.data
        spec_char = set(punctuation)

        if self.user.is_password_used(passwd):
            raise ValidationError('Invalid password, please create a different one!')

        if len(passwd) < 8:
            raise ValidationError('Password length should be at least 8 characters!')

        if len(passwd) > 50:
            raise ValidationError('Password length should be greater than 50 characters!')

        if not any(char.isdigit() for char in passwd):
            raise ValidationError('Password should have at least one number!')

        if not any(char.isupper() for char in passwd):
            raise ValidationError('Password should have at least one uppercase letter!')

        if not any(char.islower() for char in passwd):
            raise ValidationError('Password should have at least one lowercase letter!')

        if not any(char in spec_char for char in passwd):
            raise ValidationError('Password should have at least one special character!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'autocomplete': 'off'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TwoFactorAuthForm(FlaskForm):
    code = IntegerField('Enter code provided in confirmation email.')
    submit = SubmitField('Submit')


class DaycareRegistrationForm(FlaskForm):
    name = StringField('Daycare name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'autocomplete': 'off'})
    phone = StringField('Phone no.', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    capacity = IntegerField('Capacity')
    opening_time = TimeField('Opening Time')
    closing_time = TimeField('Closing Time')
    profile_pic = FileField('Profile Picture')
    submit = SubmitField('Submit')


class AddChildForm(FlaskForm):
    name = StringField('Child name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChildRequestForm(FlaskForm):
    child = SelectField('Child name', coerce=int, validators=[DataRequired(), validate_select])
    message = TextAreaField('Message')
    submit = SubmitField('Submit')
