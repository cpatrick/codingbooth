import zmq
import json


def request_compile(cur_id):
    request = json.dumps({'type': 'compile', 'id': cur_id})
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(request)
    return socket.recv()


def request_run(cur_id):
    request = json.dumps({'type': 'run', 'id': cur_id})
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(request)
    return socket.recv()
