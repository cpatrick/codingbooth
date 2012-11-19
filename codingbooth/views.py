from flask import render_template
from flask import jsonify
from flask import request

import json

from codingbooth import app, db, messenger


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile():
    code = request.form['code']
    cur_id = db.set_code(code=code)
    json_output = messenger.request_compile(cur_id)
    output = json.loads(json_output)
    return jsonify(id=cur_id, output=output)


@app.route('/run', methods=['POST', 'GET'])
def run():
    cur_id = request.form['id']
    json_output = messenger.request_run(cur_id)
    output = json.loads(json_output)
    return jsonify(id=cur_id, output=output)
