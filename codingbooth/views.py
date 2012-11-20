from flask import render_template
from flask import jsonify
from flask import request

import json

from codingbooth import app, db, messenger


@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/compile', methods=['POST'])
def compile():
    code = request.form['code']
    cur_id = None
    if 'id' in request.form:
        cur_id = request.form['id']
    cur_id = db.set_code(object_id=cur_id, code=code)
    json_output = messenger.request_compile(cur_id)
    output = json.loads(json_output)
    return jsonify(id=cur_id, output=output)


@app.route('/run', methods=['POST', 'GET'])
def run():
    cur_id = request.form['id']
    json_output = messenger.request_run(cur_id)
    output = json.loads(json_output)
    return jsonify(id=cur_id, output=output)
