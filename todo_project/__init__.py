from flask import Flask  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_login import LoginManager  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_migrate import Migrate  # type: ignore 
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)


migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)


from todo_project import routes
from todo_project import models
from todo_project import forms
