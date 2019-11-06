from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS
from datetime import datetime
from decimal import Decimal
from .model import MyUser, MyTask, db

app = Flask(__name__)
CORS(app)


def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./flask_sqlalchemy_test.db"
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    return app


@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"Message": "Welcome to TODOs app!"})


@app.route('/users', methods=['GET'])
def get_users():

    users = MyUser.query.all()

    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = MyUser.query.filter_by(id=user_id).first()

    return jsonify(user)


@app.route('/users', methods=['POST'])
def save_user():

    data = request.get_json()

    new_user = MyUser(username=data["username"], email=data["email"])

    db.session.add(new_user)

    db.session.commit()

    return jsonify(new_user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = MyUser.query.filter_by(id=user_id).first()

    db.session.delete(user)

    db.session.commit()

    return jsonify({})


@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_tasks(user_id):

    user = MyUser.query.filter_by(id=user_id).first()

    output = [] if user is None else user.tasks.all()

    return jsonify(output)


@app.route('/users/<int:user_id>/tasks', methods=['POST'])
def save_task(user_id):

    data = request.get_json()

    new_task = MyTask(content=data["content"], user_id=user_id)

    db.session.add(new_task)

    db.session.commit()

    return jsonify(new_task)


@app.route('/users/<int:user_id>/tasks/<int:task_id>', methods=['PUT'])
def update_task(user_id, task_id):

    data = request.get_json()

    task = MyTask.query.filter_by(id=task_id, user_id=user_id).first()

    task.content = data["content"]
    task.checked = data["checked"]

    db.session.add(task)

    db.session.commit()

    return jsonify(task)


@app.route('/users/<int:user_id>/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(user_id, task_id):

    task = MyTask.query.filter_by(id=task_id, user_id=user_id).first()

    db.session.delete(task)

    db.session.commit()

    return jsonify({})


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):

        if hasattr(obj, "serialize"):
          return obj.serialize()

        try:
            if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
                return obj.isoformat()
            if isinstance(obj, Decimal):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


if __name__ =="__main__":
  app.run(debug=True, port=8000)