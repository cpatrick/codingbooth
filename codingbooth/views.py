from flask import render_template
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort

import json

from codingbooth import app, db, messenger


@app.route('/')
@app.route('/<name>')
def index(name=None):
    if name:
        print name
        full_code = db.get_code_from_name(name)
        cur_id = str(full_code['_id'])
        code = full_code['code']
        return render_template('index.html', name=name, cur_id=cur_id, code=code)
    else:
        return render_template('index.html')


@app.route('/input/<cur_id>.png')
def input_image(cur_id=None):
    if cur_id:
        full_code = db.get_full_code(cur_id)
        img_doc = full_code['inputs'][0]
        resp = make_response(img_doc['contents'])
        resp.headers['Content-Type'] = 'image/png'
        return resp
    else:
        abort(404)


@app.route('/output/<cur_id>.png')
def output_image(cur_id=None):
    if cur_id:
        full_code = db.get_full_code(cur_id)
        img_doc = full_code['outputs'][0]
        resp = make_response(img_doc['content'])
        resp.headers['Content-Type'] = 'image/png'
        return resp
    else:
        abort(404)

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
