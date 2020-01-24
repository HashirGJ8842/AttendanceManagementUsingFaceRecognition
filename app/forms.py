from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), length(min=2, max=10)])
    lastName = StringField('Last Name', validators=[DataRequired(), length(min=2, max=10)])
    employee_id = IntegerField('Employee ID')

    submit = SubmitField('Register Employee')


class AdminRegister(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), length(min=2, max=10)])
    lastName = StringField('Last Name', validators=[DataRequired(), length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register Admin')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class AddLocationForm(FlaskForm):
    location_id = StringField('ID For Location', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    minimum_required = IntegerField('Minimum Employees Required', validators=[DataRequired()])
    maximum_required = IntegerField('Maximum Employees Required', validators=[DataRequired()])

    submit = SubmitField('Add Location')
