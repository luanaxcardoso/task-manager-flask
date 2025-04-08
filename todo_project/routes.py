from flask import render_template, url_for, flash, redirect, request # type: ignore
from todo_project import app, db, bcrypt

from todo_project.forms import (LoginForm, RegistrationForm, UpdateUserInfoForm, 
                                UpdateUserPassword, TaskForm, UpdateTaskForm)

from todo_project.models import User, Task

# Import 
from flask_login import login_required, current_user, login_user, logout_user # type: ignore

@app.errorhandler(404)
def error_404(error):
    return (render_template('errors/404.html'), 404)

@app.errorhandler(403)
def error_403(error):
    return (render_template('errors/403.html'), 403)

@app.errorhandler(500)
def error_500(error):
    return (render_template('errors/500.html'), 500)


@app.route("/")
def home():
    return render_template('home.html', title='Página Inicial')

@app.route("/about")
def about():
    return render_template('about.html', title='Sobre')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
       
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('all_tasks'))
        else:
            flash('Falha no login. Verifique o nome de usuário ou a senha', 'danger')
    
    return render_template('login.html', title='Entrar', form=form)

    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada para {form.username.data}', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registrar', form=form)



@app.route("/all_tasks")
@login_required
def all_tasks():
    tasks = User.query.filter_by(username=current_user.username).first().tasks
    return render_template('all_tasks.html', title='Todas as tarefas', tasks=tasks)


@app.route("/add_task", methods=['POST', 'GET'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.task_name.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        print(f"[INFO] Tarefa adicionada: '{form.task_name.data}' por {current_user.username}")
        flash('Tarefa criada!', 'success')
        return redirect(url_for('add_task'))
    return render_template('add_task.html', form=form, title='Adicionar tarefa')


@app.route("/all_tasks/<int:task_id>/update_task", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = UpdateTaskForm()
    if form.validate_on_submit():
        if form.task_name.data != task.content:
            task.content = form.task_name.data
            db.session.commit()
            flash('Tarefa atualizada', 'success')
            return redirect(url_for('all_tasks'))
        else:
            flash('Nenhuma alteração feita', 'warning')
            return redirect(url_for('all_tasks'))
    elif request.method == 'GET':
        form.task_name.data = task.content
    return render_template('add_task.html', title='Atualizar Tarefa', form=form)



@app.route("/all_tasks/<int:task_id>/delete_task")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa deletada', 'info')
    return redirect(url_for('all_tasks'))


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:  
            current_user.username = form.username.data
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 

    return render_template('account.html', title='Configurações da conta', form=form)


@app.route("/account/change_password", methods=['POST', 'GET'])
@login_required
def change_password():
    form = UpdateUserPassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Senha alterada com sucesso', 'success')
            return redirect(url_for('account'))
        else:
            flash('Por favor, insira a senha correta', 'danger')

    return render_template('change_password.html', title='Alterar Senha', form=form)

