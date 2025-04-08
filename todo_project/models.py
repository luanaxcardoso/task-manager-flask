from todo_project import db, login_manager
from datetime import datetime
from flask_login import UserMixin # type: ignore
from datetime import datetime, timezone
import pytz


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from datetime import datetime, timezone
br_tz = pytz.timezone('America/Sao_Paulo')
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(br_tz))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(br_tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.content}', '{self.date_posted}', '{self.user_id}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"
