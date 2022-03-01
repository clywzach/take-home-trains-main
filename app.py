import sys
from flask import Flask, Response, jsonify, request

from database.db import Database
from service_requests import *
from service_responses import *
from services import Services

app = Flask(__name__)
db = Database()
service = Services()

@app.route('/')
def init():
    return "OK"

@app.route('/trains', methods=['POST'])
def add_train():
    try:
        # attempt to create request object to verify request
        add_request = Add_request(**request.get_json())
    except:
        # bad user request
        return jsonify("Invalid request"), 400
    else:
        add_response = service.add_train(add_request)
        if add_response.success:
            # request succeeded
            return jsonify(add_response.message), add_response.typecode
        else: 
            # error processing request
            return jsonify(add_response.message), add_response.typecode

@app.route('/trains/<string:train_id>')
def get_schedule(train_id):
    try:
        # attempt to create request object to verify request
        schedule_request = Schedule_request(request.view_args['train_id'])
    except:
        # bad user request
        return jsonify("Invalid request"), 400
    else:
        schedule_response = service.get_schedule(schedule_request)
        if schedule_response.success:
            # request succeeded
            return jsonify(schedule_response.schedule), schedule_response.typecode
        else:
            # error processing request
            return jsonify(schedule_response.message), schedule_response.typecode

@app.route('/trains/next')
def get_next():
    time = request.headers.get('time')
    try:
        # attempt to create request object to verify request
        next_request = Next_request(time)
    except:
        # bad user request
        return jsonify("Invalid request"), 400
    else:
        next_response = service.get_next(next_request)

        if next_response.success:
            # request succeeded
            return jsonify(next_response.time), next_response.typecode
        else:
            # error processing request
            return jsonify(next_response.message), next_response.typecode

if __name__ == '__main__':
    app.run()
