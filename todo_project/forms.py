from flask_wtf import FlaskForm # type: ignore

from wtforms import StringField, PasswordField, TextAreaField, SubmitField # type: ignore

from wtforms.validators import DataRequired, EqualTo, Length, ValidationError # type: ignore

from todo_project.models import User

from flask_login import current_user # type: ignore


class RegistrationForm(FlaskForm):
    username = StringField(label='Nome de Usuário', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Senha', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Cadastrar')

   
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Usuário já existe! ')


class LoginForm(FlaskForm):
    username = StringField(label='Nome de Usuário', validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField(label='Senha', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')


class UpdateUserInfoForm(FlaskForm):
    username = StringField(label='Nome de Usuário', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField(label='Atualizar Informações')

    
    def validate_username(self, username):
        if username.data != current_user.username:    
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Esse usuário já existe!')


class UpdateUserPassword(FlaskForm):
    old_password = PasswordField(label='Digite a senha antiga', validators=[DataRequired()])
    new_password = PasswordField(label='Digite a nova senha', validators=[DataRequired()])
    submit = SubmitField(label='Alterar senha')


class TaskForm(FlaskForm):
    task_name = StringField(label='Descriçao da tarefa', validators=[DataRequired()])
    submit = SubmitField(label='Adicionar tarefa')

class UpdateTaskForm(FlaskForm):
    task_name = StringField(label='Atualizar a descrição da tarefa', validators=[DataRequired()])
    submit = SubmitField(label='Salvar alteração')