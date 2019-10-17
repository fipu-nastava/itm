from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

_db_uri = "sqlite:///./flask_sqlalchemy_test.db"
# _db_uri = "mysql://root:@localhost/flask_sqlalchemy_test" # pip install mysqlclient

app.config['SQLALCHEMY_DATABASE_URI'] = _db_uri


db = SQLAlchemy(app)


class MyUser(db.Model):

    __tablename__ = "my_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    tasks = db.relationship('MyTask', back_populates='user', lazy="dynamic")

    def __init__(self, **kwargs):
        super(MyUser, self).__init__(**kwargs)


class MyTask(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('my_user.id'), nullable=False)

    user = db.relationship('MyUser', back_populates='tasks', lazy=True)


# Kreiranje i brisanje baze
db.drop_all()
db.create_all()


# Dodavanje podataka
admin = MyUser(username='admin', email='admin@example.com')
guest = MyUser(username='guest', email='guest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()
MyUser.query.all()


# Brisanje podatka i commit
db.session.delete(MyUser.query.first())
db.session.commit()
MyUser.query.all()


# Brisanje podatka i rollback
db.session.delete(MyUser.query.first())
db.session.rollback()
MyUser.query.all()


# Ažuriranje podatka
admin = MyUser.query.filter_by(username='admin').first()
print(admin.username, admin.email)
admin.email = "admin.admin@example.com"
db.session.commit()


# Izvođenje custom SQL upita
result = db.engine.execute("Select * FROM my_user ORDER BY username")
for r in result:
    print(dict(r.items()))


# Definiranje veze preko dodatnog parametra
task = MyTask(content="Neki random task", user=admin)
print(admin.tasks.all())
db.session.add(task)
db.session.commit()

# Definiranje veze preko liste detalja
task2 = MyTask(content="Random task 2")
admin.tasks.append(task2)
db.session.add(admin)
db.session.commit()

# Definiranje veze preko reference na mastera
task3 = MyTask(content="Random task 3")
task3.user = admin
db.session.add(admin)
db.session.commit()

admin = MyUser.query.filter_by(username='admin').first()
admin.tasks

# Dohvaćanje podataka
MyUser.query.all()
MyUser.query.first().tasks
MyUser.query.first().tasks.all()


# Ispis query-a
print(MyUser.query)
print(MyUser.query.first().tasks)