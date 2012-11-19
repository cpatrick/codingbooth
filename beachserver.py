import zmq
import json
from codingbooth import db
import subprocess
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    request = json.loads(message)

    request_type = request['type']
    code_id = request['id']

    if request_type == 'compile':

        code = db.get_code(code_id)
        print code  # DEBUG

        code_file_name = '%s.cpp' % code_id
        code_file = file(code_file_name, 'w')
        code_file.write(code)
        code_file.close()

        compile_runner = subprocess.Popen(['/usr/bin/gcc', code_file_name,
            '-o', '%s.out' % code_id],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        compile_output = compile_runner.communicate()[0]
        db.set_compile_results(code_id, compile_output)

        json_output = json.dumps({'status': 1, 'output': compile_output})

        #  Send reply back to client
        socket.send(json_output)

        os.unlink(code_file_name)
    elif request_type == 'run':
        compile_runner = subprocess.Popen(['./%s.out' % code_id],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        run_output = compile_runner.communicate()[0]
        db.set_run_results(code_id, run_output)

        json_output = json.dumps({'status': 1, 'output': run_output})

        socket.send(json_output)
