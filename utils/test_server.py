
import json
from flask import Flask

INDEX_DATA = dict(
    users = [
        dict(id='1', username='admin'),
        dict(id='2', username='john.doe'),
        ],
    projects = [
        dict(id='1', label='my_project', user='1'),
        dict(id='2', label='some_other_project', user='2'),
        ]
    )

GET_ALL_DATA = dict(
    objects = [
        dict(id='1', username='admin'),
        dict(id='2', username='john.doe'),
        ]
    )
    
GET_ONE_DATA = dict(id='1', username='admin'),

app = Flask(__name__)

def render(code, data):
    response = jsonify(message=data)
    response.status_code = (code)
    return response
    
@app.route("/")
def index():
    return json.dumps(INDEX_DATA)

@app.route("/users/")
def get():
    return json.dumps(GET_ALL_DATA)

@app.route("/users/1/")
def get_one():
    return json.dumps(GET_ONE_DATA)


if __name__ == "__main__":
    app.run()