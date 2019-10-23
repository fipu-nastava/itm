from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class MyUser(db.Model):

    __tablename__ = "my_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    tasks = db.relationship('MyTask', back_populates='user', lazy="dynamic")

    def __init__(self, **kwargs):
        super(MyUser, self).__init__(**kwargs)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }


class MyTask(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('my_user.id'), nullable=False)

    user = db.relationship('MyUser', back_populates='tasks', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at
        }



