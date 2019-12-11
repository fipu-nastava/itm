from flask import Flask, jsonify
from flask_cors import CORS
from .task_ai import predict

app = Flask(__name__)
CORS(app)


def create_app():
    return app


@app.route('/predict/<string:task>', methods=['GET'])
def predict_task(task):
    return jsonify({"predicted": predict(task)})
