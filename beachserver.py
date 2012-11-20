import zmq
import json
from codingbooth import db
import subprocess
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

sandbox_path = '/Users/cpatrick/Source/codingbooth'


def compile_with_cmake(object_id):
    os.chdir(sandbox_path)
    code_doc = db.get_full_code(object_id)
    if not os.path.exists(object_id):
        os.mkdir(object_id)
    code_dir_path = os.path.abspath(object_id)
    code_file_name = os.path.join(code_dir_path, 'test.cxx')
    cmake_file_name = os.path.join(code_dir_path, 'CMakeLists.txt')
    with open(code_file_name, 'w') as outfile:
        outfile.write(code_doc['code'])
    with open(cmake_file_name, 'w') as outfile:
        outfile.write(code_doc['cmake'])
    for cur_input in code_doc['inputs']:
        cur_file_name = os.path.join(code_dir_path, cur_input['name'])
        with open(cur_file_name, 'w') as outfile:
            outfile.write(cur_input['contents'])

    os.chdir(code_dir_path)
    cmake_runner = subprocess.Popen(['/usr/local/bin/cmake', code_dir_path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    make_runner = subprocess.Popen(['/usr/bin/make'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmake_output = cmake_runner.communicate()[0]
    make_output = make_runner.communicate()[0]
    return "%s\n%s" % (cmake_output, make_output)


def run_from_cmake(object_id):
    os.chdir(sandbox_path)
    code_dir_path = os.path.abspath(object_id)
    os.chdir(code_dir_path)
    test_runner = subprocess.Popen(['./test'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    run_output = test_runner.communicate()[0]
    return run_output

while True:
    message = socket.recv()
    request = json.loads(message)

    request_type = request['type']
    code_id = request['id']

    code_doc = db.get_full_code(code_id)

    if request_type == 'compile':

        if 'cmake' in code_doc:
            compile_output = compile_with_cmake(code_id)
        else:
            code = code_doc['code']
            print code  # DEBUG

            code_file_name = '%s.cpp' % code_id
            code_file = file(code_file_name, 'w')
            code_file.write(code)
            code_file.close()

            compile_runner = subprocess.Popen(['/usr/bin/gcc', code_file_name,
                '-o', '%s.out' % code_id],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            compile_output = compile_runner.communicate()[0]
            os.unlink(code_file_name)

        db.set_compile_results(code_id, compile_output)
        json_output = json.dumps({'status': 1, 'output': compile_output})

        #  Send reply back to client
        socket.send(json_output)

    elif request_type == 'run':
        if 'cmake' in code_doc:
            run_output = run_from_cmake(code_id)
        else:
            compile_runner = subprocess.Popen(['./%s.out' % code_id],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            run_output = compile_runner.communicate()[0]
        db.set_run_results(code_id, run_output)

        json_output = json.dumps({'status': 1, 'output': run_output})

        socket.send(json_output)
