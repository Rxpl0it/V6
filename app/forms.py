from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, Email
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    file = FileField('File', validators=[FileRequired()])
    category = SelectField('Category', choices=[('tools', 'Tools'), ('combo', 'Combo'), ('tutorials', 'Tutorials'), ('shop', 'Shop')], validators=[DataRequired()])
    price = FloatField('Price', validators=[Optional()])
    purchase_link = StringField('Purchase Link', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Create Post')