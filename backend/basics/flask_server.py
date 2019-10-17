from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)


def _html(message):
    return "<html><body><h1>{0}</h1></body></html>".format(message)

@app.route('/', methods=["GET"])
def home():
  return _html("Home page!")

@app.route('/', methods=["POST"])
def home_post():
  return _html("POST!")

@app.route('/', methods=["PATCH"])
def home_patch():
  return _html("PATCH!")

@app.route('/', methods=["DELETE"])
def home_delete():
  return _html("DELETE!")

@app.route('/test', methods=["GET"])
def test():
  return _html("Test page!")

@app.route('/test2', methods=["GET"])
def test2():
  return _html("Test page 2!")

@app.route('/test3', methods=["POST"])
def test3():
  return _html("Test page 3, it should fail!")

@app.route('/users/<string:username>', methods=['GET'])
def get_user(username):

  # TODO: ovdje treba napraviti dohvaćanje iz baze podataka

  output = {"username": username, "email": username + "@gmail.com"}

  return jsonify(output)


@app.route('/users', methods=['POST'])
def save_user():

  data = request.get_json()

  #print(data)

  username = data["username"]
  email = data["email"]
  created_at = datetime.now()

  output = {"username": username, "email": email, "created_at": created_at}

  return jsonify(output)



### <Custom class>

class AppUser:
  def __init__(self, username, email, created_at):
    self.username = username
    self.email = email
    self.created_at = created_at

  def serialize(self):
    return {
      'username': self.username,
      'email': self.email,
      'created_at': self.created_at
    }


@app.route('/users/<username>/class', methods=['GET'])
def get_user_class(username):

  output = AppUser(username, username + "@gmail.com", datetime.now())

  return jsonify(output)


@app.route('/users/<username>/class2', methods=['GET'])
def get_users_class(username):

    user = AppUser(username, username + "@gmail.com", datetime.now())

    output = [user for i in range(10)]

    return jsonify(output)

### </Custom class>



### <Custom JSON Encoder>

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

### </Custom JSON Encoder>


if __name__ =="__main__":
  app.run(debug=True, port=8000)