#!/usr/bin/env python

import json
import sys
import threading
from flask import Flask, request

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
    
app = Flask(__name__)

@app.route("/")
def index():
    return json.dumps(INDEX_DATA)

@app.route("/users/<pk>/", methods=['GET', 'PUT', 'DELETE'])
def get_put_delete(pk):
    if request.method == 'GET':
        DATA = dict(
            method='GET',
            action='get_one',
            id='1', 
            username='admin'
            )
        return json.dumps(DATA)
    elif request.method == 'PUT':
        DATA = dict(
            method='PUT',
            action='put',
            )
        return json.dumps(DATA)
    elif request.method == 'DELETE':
        DATA = dict(
            method='DELETE',
            action='delete',
            )
        return json.dumps(DATA)
        
@app.route('/users/', methods=['GET', 'POST'])
def get_all_or_post():
    if request.method == 'GET':
        DATA = dict(
            method=request.method,
            action='get_all',
            objects=[
                dict(id='1', username='admin'),
                dict(id='2', username='john.doe'),
                ]
            )

        return json.dumps(DATA)
    elif request.method == 'POST':
        DATA = dict(
            method='POST',
            )
        return json.dumps(DATA)
    
if __name__ == "__main__":  
    app.run()