from flask_wtf import FlaskForm # type: ignore

# Form Fields
from wtforms import StringField, PasswordField, TextAreaField, SubmitField # type: ignore

# Form Validators for Form fields
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError # type: ignore

# Import the User Database Model
from todo_project.models import User

from flask_login import current_user # type: ignore


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Register')

    # serve para verificar se o username já existe no banco de dados
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Exists')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class UpdateUserInfoForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField(label='Update Info')

    # serve para verificar se o username já existe no banco de dados
    def validate_username(self, username):
        if username.data != current_user.username:    
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Exists')


class UpdateUserPassword(FlaskForm):
    old_password = PasswordField(label='Enter Old Password', validators=[DataRequired()])
    new_password = PasswordField(label='Enter New Password', validators=[DataRequired()])
    submit = SubmitField(label='Change password')


class TaskForm(FlaskForm):
    task_name = StringField(label='Task Description', validators=[DataRequired()])
    submit = SubmitField(label='Add Task')

class UpdateTaskForm(FlaskForm):
    task_name = StringField(label='Update Task Description', validators=[DataRequired()])
    submit = SubmitField(label='Save Changes')
