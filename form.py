from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf.file import FileAllowed
import sqlalchemy as sa
from models import db, User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Full Name', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        query = sa.select(User).where(User.username == username.data)
        user = db.session.scalar(query)
        if user is not None:
            raise ValidationError('Username already exists, please use a different one.')

    def validate_email(self, email):
        query = sa.select(User).where(User.email == email.data)
        user = db.session.scalar(query)
        if user is not None:
            raise ValidationError('Email already registered, please use a different one.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio      = TextAreaField('Bio', validators=[Length(min=0, max=140)])
    location = StringField('Location', validators=[DataRequired()])
    name     = StringField('Full Name', validators=[DataRequired()])

    def __init__(self, original_username=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')

class ProfileForm(FlaskForm):
    display_name = StringField('Display Name', validators=[DataRequired()])
    username     = StringField('Username', validators=[DataRequired()])
    email        = StringField('Email', validators=[DataRequired(), Email()])

class CourseForm(FlaskForm):
    course_code = StringField('', validators= [DataRequired()])
    credit_unit = StringField('', validators= [DataRequired()])
    material = FileField('', validators= [FileAllowed(["pdf"], "")])
    status = SelectField ('', choices=['Required' '', 'Core' '', 'Elective' ''])

class AddMaterial(FlaskForm):
    material = FileField('', validators= [FileAllowed(["pdf"], "")])
    courseID = StringField('', validators= [DataRequired()])
    

    